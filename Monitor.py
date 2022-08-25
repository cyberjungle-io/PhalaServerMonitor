import requests
import json
import LinuxMonitor
import PhalaMonitor
import PhalaBlockChain
import time
import ExecCmd


with open("./config/config.json") as file:
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
        "HostName": "phala1",
        "PhalaData": PhalaMonitor.getPhala(PhalaServicesBaseUrl),
        "PolkadotData": PhalaMonitor.getPolkadot(PhalaServicesBaseUrl),
        "Pruntime":PhalaMonitor.getPruntime(PhalaServicesBaseUrl),
        "DockerContainers": {},
        "LinuxData": {},
        "Gas": gas

    }

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


    time.sleep(UpdateInterval)
    
