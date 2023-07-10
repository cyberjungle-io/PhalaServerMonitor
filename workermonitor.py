import requests
import json
import LinuxMonitor
import PhalaMonitor
import PhalaBlockChain
import time
import math
import ExecCmdWorker


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

doLoop = True

while doLoop:
    
    result = {
        "monitorType": monitorType,
        "serviceName": serviceName,
        "interval": interval,
        "org_id" : monitorKey,
        "nodeBaseUrl": nodeBaseUrl,
        "updateTime": math.trunc(time.time()*1000),
        "hostName": LinuxMonitor.getHostName(),
        "pruntime":PhalaMonitor.getPruntime(nodeBaseUrl),
        "dockerContainers": LinuxMonitor.getDockerList(),
        "linuxData": LinuxMonitor.getLinuxData(),
        

    } 

    print(result)

    data_json = json.dumps(result)
    url = monitorUrl + "/worker/updatePrbWorker"
    headers = {'Content-type': 'application/json','monitor_key':monitorKey} 
    try:
        r = requests.post(url, data=data_json, headers=headers,timeout=30)
        rest_result = r.json()
        print(rest_result)
       # khala = r.json()["result"]
        for cmd in rest_result["commands"]:
            print(cmd["command"])
            logdata = {
                 "command": cmd["command"],
                 "monitorType": monitorType,
                 "serviceName": serviceName,
                 "org_id" : monitorKey,
                 "timestamp": math.trunc(time.time()*1000)
            }
            if cmd["command"] == "update phala":
                ExecCmdWorker.SendPhalaUpdate()

            if cmd["command"] == "restart phala":
                ExecCmdWorker.SendPhalaRestart()
                

            if cmd["command"] == "autorestart phala":
                
                logdata["phalaStatus"] = result
                tlogs = {
                         "phala-pruntime":LinuxMonitor.get_docker_logs('~/solo-mining-scripts-main/docker-compose.yml',"phala-pruntime",100),
                         }
                logdata["dockerLogs"] = tlogs
                ExecCmdWorker.SendPhalaRestart()

            if cmd["command"] == "stop phala":
                ExecCmdWorker.SendPhalaStop()

            if cmd["command"] == "start phala":
                ExecCmdWorker.SendPhalaStart()

            if cmd["command"] == "update monitor":
                ExecCmdWorker.UpdateMonitor()
                doLoop = False

            
            if cmd["command"] == "phala logs":
                logdata["phalaStatus"] = result
                tlogs = {
                        "phala-pruntime":LinuxMonitor.get_docker_logs('~/worker/docker-compose.yml',"phala-pruntime",100),
                }
                logdata["dockerLogs"] = tlogs

            
            data_json = json.dumps(logdata)
            print(data_json)
            url = monitorUrl + "/worker/saveWorkerLog"
            rc = requests.post(url, data=data_json, headers=headers,timeout=30)
     
       
    except:
        khala = {}


    time.sleep(interval)
    
