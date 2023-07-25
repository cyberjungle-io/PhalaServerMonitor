#!/usr/bin/env bash

function phala_scripts_install_aptdependencies() {
  if [ "$1" == "uninstall" ];then
    shift
    phala_scripts_log info "Uninstall Apt dependencies" cut
    apt autoremove -y $*
    return 0
  fi

  _default_soft=$*
  phala_scripts_log info "Apt update" cut
  apt update
  if [ $? -ne 0 ]; then
    phala_scripts_log error "Apt update failed."
  fi
  phala_scripts_log info "Installing Apt dependencies" cut
  apt install -y ${_default_soft[@]}
}

function phala_scripts_install_otherdependencies(){
  if [ "$1" == "uninstall" ];then
    shift
    phala_scripts_log info "Uninstall other dependencies" cut
    for _package in $*;do
      if ! type $_package > /dev/null 2>&1;then
        :
      else
        case $_package in
          docker)
            apt autoremove -y docker-ce docker-ce-cli
            find /etc/apt/sources.list.d -type f -name docker.list* -exec rm -f {} \;
          ;;
          docker-compose)
            [ -f /usr/local/bin/docker-compose ] && rm -rf /usr/local/bin/docker-compose
          ;;
          node)
            apt autoremove -y nodejs
            find /etc/apt/sources.list.d -type f -name nodesource.list* -exec rm -f {} \;
          ;;
          *)
            apt autoremove -y $_package
          ;;
        esac
      fi
    done
    return 0
  fi

  _other_soft=$*
  phala_scripts_log info "Installing other dependencies" cut
  for _package in ${_other_soft};do
    if ! type $_package >/dev/null 2>&1;then
      case $_package in
        docker-compose)
          if [ ! -f /usr/local/bin/docker-compose ];then
            if [ "${PHALA_LANG}" == "CN" ];then
              # curl -L "https://get.daocloud.io/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o ${phala_scripts_tmp_dir}/docker-compose && \
              curl -L "${phala_scripts_install_docker_compose_cn}" -o ${phala_scripts_tmp_dir}/docker-compose && \
              mv ${phala_scripts_tmp_dir}/docker-compose /usr/local/bin/
            else
              # curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o ${phala_scripts_tmp_dir}/docker-compose && \
              curl -L "${phala_scripts_install_docker_compose}" -o ${phala_scripts_tmp_dir}/docker-compose && \
              mv ${phala_scripts_tmp_dir}/docker-compose /usr/local/bin/
            fi
          fi
          chmod +x /usr/local/bin/docker-compose
        ;;
        docker)
          find /etc/apt/sources.list.d -type f -name docker.list.* -exec rm -f {} \;
          if [ ! -f "${phala_scripts_tools_dir}/get-docker.sh" ];then
            curl -fsSL get.docker.com -o ${phala_scripts_tools_dir}/get-docker.sh
          fi

          # set cn
          if [ "${PHALA_LANG}" == "CN" ];then
            bash ${phala_scripts_tools_dir}/get-docker.sh --mirror Aliyun || :
            # # disable cn; error
            # systemctl stop docker.socket
            # [ -d /etc/docker ] || mkdir /etc/docker
            # printf '{\n  "registry-mirrors": [\n    "https://docker.mirrors.ustc.edu.cn"\n  ]\n}' > /etc/docker/daemon.json
            # systemctl start docker.socket

          else
            bash ${phala_scripts_tools_dir}/get-docker.sh || :
          fi
          type docker || phala_scripts_log "Docker Install Fail"
        ;;
        node)
          find /etc/apt/sources.list.d -type f -name 'nodesource.list.*' -exec rm -f {} \;
          if [ ! -f "${phala_scripts_tools_dir}/get-node.sh" ];then
            # curl -fsSL https://deb.nodesource.com/setup_lts.x -o ${phala_scripts_tools_dir}/get-node.sh
            curl -fsSL ${phala_scripts_install_setupnode} -o ${phala_scripts_tools_dir}/get-node.sh
          fi
          bash ${phala_scripts_tools_dir}/get-node.sh
          apt-get install -y nodejs
        ;;
      esac
    fi
  done

}

function phala_scripts_install_sgx() {
  _kernel_version=$(uname -r)
  if [ -c /dev/sgx_enclave ];then
    phala_scripts_install_sgx_default
  elif [ ${DISTRIB_RELEASE} == "20.04" ];then
    phala_scripts_install_sgx_k5_4 && \
    phala_scripts_install_sgx_default
  elif [ ${DISTRIB_RELEASE} == "18.04" ];then
    phala_scripts_install_sgx_k5_4
  fi

}

function phala_scripts_install_sgx_default() {
  # install aesm encalave
  # curl -fsSL https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key | apt-key add - && \
  curl -fsSL ${phala_scripts_install_intel_sgx_deb} | apt-key add - && \
  # add-apt-repository -y "deb https://download.01.org/intel-sgx/sgx_repo/ubuntu focal main" && \
  add-apt-repository -y "${phala_scripts_install_intel_addapt_deb}" && \
  # reinstall : fix apt upgrade
  # 21.10 sgx-aesm-service error skip aesm
  # apt reinstall -y libsgx-enclave-common sgx-aesm-service
  apt autoremove -y libsgx-enclave-common
  apt install -y libsgx-enclave-common

}

function phala_scripts_install_sgx_k5_4(){

  type make dkms >/dev/null 2>&1 || apt install -y make dkms

  # _intel_base_url="https://download.01.org/intel-sgx/latest/linux-latest/distro/ubuntu20.04-server"
  # _dcap_driver_url="$(curl -fsSL ${intel_base_url}/driver_readme.txt|grep -vE "^$"|awk -F':' '/DCAP driver/ {print $2}'|sed 's/ //g')"
  # _oot_driver_url="$(curl -fsSL ${intel_base_url}/driver_readme.txt|grep -vE "^$"|awk -F':' '/OOT driver/ {print $2}'|sed 's/ //g')"

  [ -f ${phala_scripts_tools_dir}/sgx_linux_x64_driver_1.41.bin ] || {
    # curl -fsSL https://download.01.org/intel-sgx/latest/linux-latest/distro/ubuntu20.04-server/sgx_linux_x64_driver_1.41.bin -o ${phala_scripts_tmp_dir}/sgx_linux_x64_driver_1.41.bin && \
    curl -fsSL ${phala_scripts_install_intel_old_device} -o ${phala_scripts_tmp_dir}/sgx_linux_x64_driver_1.41.bin && \
    mv ${phala_scripts_tmp_dir}/sgx_linux_x64_driver_1.41.bin ${phala_scripts_tools_dir}/
  }
  bash ${phala_scripts_tools_dir}/sgx_linux_x64_driver_1.41.bin || echo
  # curl -fsSL https://download.01.org/intel-sgx/latest/linux-latest/distro/ubuntu20.04-server/sgx_linux_x64_driver_2.11.054c9c4c.bin -o ${phala_scripts_tmp_dir}/sgx_linux_x64_driver_oot.bin && \
  [ -f ${phala_scripts_tools_dir}/sgx_linux_x64_driver_oot.bin ] || {
    curl -fsSL ${phala_scripts_install_intel_old_device_2_11} -o ${phala_scripts_tmp_dir}/sgx_linux_x64_driver_oot.bin && \
    mv ${phala_scripts_tmp_dir}/sgx_linux_x64_driver_oot.bin ${phala_scripts_tools_dir}/
  }
  bash ${phala_scripts_tools_dir}/sgx_linux_x64_driver_oot.bin
  # }

}



phala_scripts_utils_apt_source_cn="https://mirrors.163.com"
phala_scripts_install_docker_compose_cn="https://get.daocloud.io/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)"
phala_scripts_install_docker_compose="https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)"
phala_scripts_install_intel_sgx_deb="https://download.01.org/intel-sgx/sgx_repo/ubuntu/intel-sgx-deb.key"
phala_scripts_install_intel_addapt_deb="deb https://download.01.org/intel-sgx/sgx_repo/ubuntu focal main"
phala_scripts_install_intel_old_device="https://download.01.org/intel-sgx/latest/linux-latest/distro/ubuntu20.04-server/sgx_linux_x64_driver_1.41.bin"
# phala_scripts_install_intel_old_device_2_11="https://download.01.org/intel-sgx/latest/linux-latest/distro/ubuntu20.04-server/sgx_linux_x64_driver_2.11.0_2d2b795.bin"
phala_scripts_install_intel_old_device_2_11="https://download.01.org/intel-sgx/latest/linux-latest/distro/ubuntu20.04-server/sgx_linux_x64_driver_2.11.054c9c4c.bin"
phala_scripts_install_setupnode="https://deb.nodesource.com/setup_lts.x"
phala_scripts_headers_gethost="https://arweave.net"
phala_scripts_headers_geturl="https://raw.githubusercontent.com/Phala-Network/solo-mining-scripts/main/arindex.csv"
phala_scripts_headers_snapshot_url="https://ksm-rocksdb.polkashots.io/snapshot"


phala_scripts_install_otherdependencies docker
phala_scripts_install_otherdependencies docker-compose
phala_scripts_install_otherdependencies node


mkdir ~/node
cp node-docker-compose.yml ~/node/docker-compose.yml
