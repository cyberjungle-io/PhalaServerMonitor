import requests
import json
import LinuxMonitor
import PhalaMonitor
import PhalaBlockChain
import time
import math
import ExecCmdPrb
import Prb 


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
        "phalaData": PhalaMonitor.getPhala(nodeBaseUrl),
        "polkadotData": PhalaMonitor.getPolkadot(nodeBaseUrl), 
        "dockerContainers": LinuxMonitor.getDockerList(),
        "linuxData": LinuxMonitor.getLinuxData(),
        "prbData": Prb.getPrbWorkers(nodeBaseUrl),
        

    } 

    #print(result)

    data_json = json.dumps(result)
    url = monitorUrl + "/worker/updatePhalaNode"
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
            

            if cmd["command"] == "stop node":
                ExecCmdPrb.StopNode()

            if cmd["command"] == "start node":
                ExecCmdPrb.StartNode()

            if cmd["command"] == "restart node":
                ExecCmdPrb.RestartNode()

          
                
            
            if cmd["command"] == "prb logs":
                logdata["phalaStatus"] = result
                tlogs = {
                        
                        "node":LinuxMonitor.get_docker_logs('~/node/docker-compose.yml',"node",100),
                }
                logdata["dockerLogs"] = tlogs
            
            
            data_json = json.dumps(logdata)
            print(data_json)
            url = monitorUrl + "/worker/saveWorkerLog"
            rc = requests.post(url, data=data_json, headers=headers,timeout=30)
     
       
    except:
        khala = {}


    time.sleep(interval)
    
