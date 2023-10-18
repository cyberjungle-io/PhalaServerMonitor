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
        #"phalaData": PhalaMonitor.getPhala(nodeBaseUrl),
        #"polkadotData": PhalaMonitor.getPolkadot(nodeBaseUrl), 
        "dockerContainers": LinuxMonitor.getDockerList(),
        "linuxData": LinuxMonitor.getLinuxData(),
        "prbData": Prb.getPrbWorkers(nodeBaseUrl),
        

    } 

    #print(result)

    data_json = json.dumps(result)
    url = monitorUrl + "/worker/updatePrb"
    headers = {'Content-type': 'application/json','monitor_key':monitorKey} 
    try:
        print("1")
        r = requests.post(url, data=data_json, headers=headers,timeout=30)
        rest_result = r.json()
        print(rest_result)
        print("2")
       # khala = r.json()["result"]
        for cmd in rest_result:
            print("cmd in for loop: " + cmd["command"])
            logdata = {
                 "command": cmd["command"],
                 "monitorType": monitorType,
                 "serviceName": serviceName,
                 "org_id" : monitorKey,
                 "timestamp": math.trunc(time.time()*1000)
            }
            print("3")
            if cmd["command"] == "stop lifecycle":
                ExecCmdPrb.StopLifecycle()
            
            if cmd["command"] == "start lifecycle":
                ExecCmdPrb.StartLifecycle()

            if cmd["command"] == "restart lifecycle":
                ExecCmdPrb.RestartLifecycle()
            
            if cmd["command"] == "stop data provider":
                ExecCmdPrb.StopDataProvider()

            if cmd["command"] == "start data provider":
                ExecCmdPrb.StartDataProvider()

            if cmd["command"] == "restart data provider":
                ExecCmdPrb.RestartDataProvider()

            if cmd["command"] == "stop node":
                ExecCmdPrb.StopNode()

            if cmd["command"] == "start node":
                ExecCmdPrb.StartNode()

            if cmd["command"] == "restart node":
                ExecCmdPrb.RestartNode()

            if cmd["command"] == "stop prb":
                ExecCmdPrb.StopPrb()

            if cmd["command"] == "start prb":
                ExecCmdPrb.StartPrb()
            
            if cmd["command"] == "restart prb":
                ExecCmdPrb.RestartPrb()


            if cmd["command"] == "restart phala":
                ExecCmdPrb.SendPhalaRestart()
                
            print("4")
            if cmd["command"] == "prb logs":
                logdata["phalaStatus"] = result
                tlogs = {
                        "lifecycle":LinuxMonitor.get_docker_logs('~/lifecycle/docker-compose.yml',"lifecycle",100),
                        "redis":LinuxMonitor.get_docker_logs('~/lifecycle/docker-compose.yml',"redis-q",100),
                        "data_provider":LinuxMonitor.get_docker_logs('~/provider/docker-compose.yml',"data_provider",100),
                        "monitor":LinuxMonitor.get_docker_logs('~/provider/docker-compose.yml',"monitor",100),
                        "node":LinuxMonitor.get_docker_logs('~/node/docker-compose.yml',"node",100),
                }
                logdata["dockerLogs"] = tlogs
            print("5")
            print(cmd["command"].find("restartprbworker"))
            if cmd["command"].find("restartprbworker") >=0:
                print(cmd["command"].split("|")[1])
                Prb.restartPbrWorkers(nodeBaseUrl,cmd["command"].split("|")[1])

            
            data_json = json.dumps(logdata)
            print(data_json)
            url = monitorUrl + "/worker/saveWorkerLog"
            rc = requests.post(url, data=data_json, headers=headers,timeout=30)
     
       
    except Exception as e:
        print("An error occurred:", str(e))
        khala = {}


    time.sleep(interval)
    
