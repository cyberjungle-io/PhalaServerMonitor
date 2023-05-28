import requests
import os
import json
import LinuxMonitor
import PhalaMonitor
import PhalaBlockChain
import time
import math
import ExecCmd


with open("config.json") as file:
    phalaConfig = json.load(file)

print(phalaConfig)
monitorType = phalaConfig["monitorType"]
serviceName = phalaConfig["serviceName"]
hostName = phalaConfig["hostName"]
monitorUrl = phalaConfig["monitorUrl"]
monitorKey = phalaConfig["monitorKey"]
interval = phalaConfig["interval"]
nodeBaseUrl = phalaConfig["nodeBaseUrl"]
gasAccount = phalaConfig["gasAccount"]

#pull Env Variables from the Solo Miner.
home_dir = os.path.expanduser("~")
file_path = os.path.join(home_dir, 'solo-mining-scripts-main/.env')
with open(file_path, 'r') as file:
    # Initialize variables
    cores = None
    gas_account_address = None
    operator = None
    phala_model = None

    # Iterate over each line in the file
    for line in file:
        # Split the line by '=' to separate the variable name and value
        variable, value = line.strip().split('=')

        # Check if the variable is one of the desired ones
        if variable == 'CORES':
            cores = value
        elif variable == 'GAS_ACCOUNT_ADDRESS':
            gas_account_address = value
        elif variable == 'OPERATOR':
            operator = value
        elif variable == 'PHALA_MODEL':
            phala_model = value

soloEnv = {
     "cores": cores,
     "gasAccount": gas_account_address,
     "operator": operator,
     "phalaModel":phala_model

}


while True:
    
    result = {
        "monitorType": monitorType,
        "serviceName": serviceName,
        "interval": interval,
        "org_id" : monitorKey,
        "nodeBaseUrl": nodeBaseUrl,
        "updateTime": math.trunc(time.time()*1000),
        "hostName": LinuxMonitor.getHostName(),
        "phalaData": PhalaMonitor.getPhala(nodeBaseUrl),
        "polkadotData": PhalaMonitor.getPolkadot(nodeBaseUrl),  
        "pruntime":PhalaMonitor.getPruntime(nodeBaseUrl),
        "dockerContainers": PhalaMonitor.getPhalaServices(),
        "linuxData": LinuxMonitor.getLinuxData(),
        "soloEnv": soloEnv
        

    } 

    print(result)

    data_json = json.dumps(result)
    url = monitorUrl + "/worker/updateSoloWorker"
    headers = {'Content-type': 'application/json','monitor_key':monitorKey} 
    try:
        r = requests.post(url, data=data_json, headers=headers,timeout=30)
        result = r.json()
        print(result)
       # khala = r.json()["result"]
        if result["send_update_command"]:
            ExecCmd.SendPhalaUpdate()

        if result["send_restart_command"]:
            ExecCmd.SendPhalaRestart()

        if result["send_stop_command"]:
                ExecCmd.SendPhalaStop()

        if result["send_start_command"]:
                ExecCmd.SendPhalaStart()

        if result["send_reboot"]:
                print("send_reboot")
       
    except:
        khala = {}


    time.sleep(interval)
    
