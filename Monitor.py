import requests
import json
import LinuxMonitor
import PhalaMonitor
import time


with open("config.json") as file:
    phalaConfig = json.load(file)

print(phalaConfig)

PhalaServiceUrl = phalaConfig["PhalaServiceUrl"]
CyberJunglePhalaAccount = phalaConfig["CyberJunglePhalaAccount"]
CyberJunglePhalaKey = phalaConfig["CyberJunglePhalaKey"]
PhalaServicesBaseUrl = phalaConfig["PhalaServicesBaseUrl"]
UpdateInterval = phalaConfig["UpdateInterval"]

while True:
    
    result = {
        "HostName": LinuxMonitor.getHostName(),
        "PhalaData": PhalaMonitor.getPhala(PhalaServicesBaseUrl),
        "PolkadotData": PhalaMonitor.getPolkadot(PhalaServicesBaseUrl),
        "Pruntime":PhalaMonitor.getPruntime(PhalaServicesBaseUrl),
        "DockerContainers": PhalaMonitor.getPhalaServices()

    }
    print(result)

    data_json = json.dumps(result)
    url = PhalaServiceUrl + "/worker/updateWorker"
    headers = {'Content-type': 'application/json','monitor_id':CyberJunglePhalaAccount,'monitor_key':CyberJunglePhalaKey} 
    try:
        r = requests.post(url, data=data_json, headers=headers,timeout=30)
       # khala = r.json()["result"]
       
    except:
        khala = {}


    time.sleep(UpdateInterval)
    
