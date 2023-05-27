import requests
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
        "dockerContainers": PhalaMonitor.getPhalaServices(),
        "linuxData": LinuxMonitor.getLinuxData(),
        

    } 

    print(result)

    data_json = json.dumps(result)
    url = monitorUrl + "/worker/updatePrb"
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
    
