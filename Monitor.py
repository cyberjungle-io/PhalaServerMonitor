import requests
import json
import LinuxMonitor
import PhalaMonitor
import PhalaBlockChain
import time


with open("config.json") as file:
    phalaConfig = json.load(file)

print(phalaConfig)

PhalaServiceUrl = phalaConfig["PhalaServiceUrl"]
CyberJunglePhalaAccount = phalaConfig["CyberJunglePhalaAccount"]
CyberJunglePhalaKey = phalaConfig["CyberJunglePhalaKey"]
PhalaServicesBaseUrl = phalaConfig["PhalaServicesBaseUrl"]
UpdateInterval = phalaConfig["UpdateInterval"]
GasAccount = phalaConfig["GasAccount"]

while True:
    gas = 0
    lockedValue = 0
    if (GasAccount != ""):
        gas,lockedValue = PhalaBlockChain.getAccountBalance(GasAccount)
    result = {
        "HostName": LinuxMonitor.getHostName(),
        "PhalaData": PhalaMonitor.getPhala(PhalaServicesBaseUrl),
        "PolkadotData": PhalaMonitor.getPolkadot(PhalaServicesBaseUrl),
        "Pruntime":PhalaMonitor.getPruntime(PhalaServicesBaseUrl),
        "DockerContainers": PhalaMonitor.getPhalaServices(),
        "LinuxData": LinuxMonitor.getLinuxData(),
        "Gas": gas

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
    
