import requests
import json
import docker


    
#url = "http://localhost:9933/system_syncState"
def getPhala(baseUrl):
    url = baseUrl + ":9933"
    print(url)
    dt = {
        "id":1, "jsonrpc":"2.0", "method": "system_syncState", "params":[]
    }
    data_json = json.dumps(dt)
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=data_json, headers=headers,timeout=30)
    print(r)
    ph = r.json()["result"]

    return ph

#url = "http://localhost:9934/system_syncState"
def getPolkadot(baseUrl):
    url = baseUrl + ":9934/system_syncState"
    dt = {
        "id":1, "jsonrpc":"2.0", "method": "system_syncState", "params":[]
    }
    data_json = json.dumps(dt)
    headers = {'Content-type': 'application/json'}

    r = requests.post(url, data=data_json, headers=headers)

    Polkadot = r.json()["result"]
    
    return Polkadot



#url = "http://localhost:8000/get_info"
def getPruntime(baseUrl):
    url = baseUrl + ":8000/get_info"
    headers = {'Content-type': 'application/json'}    
    r = requests.get(url, headers=headers)    
       
    tmpjson = json.loads(r.json()["payload"])
     
    return tmpjson


def getPhalaServices():
    client = docker.from_env()

    phala = {"phalapherry":"stop",
            "phalapruntime":"stop",
            "phalanode":"stop"
    }

    #print(str(client.containers.list()))

    for container in client.containers.list():
        
        if (container.name == "phala-pherry"):
            phala["phalapherry"] = container.status
        if (container.name == "phala-pruntime"):
            phala["phalapruntime"] = container.status
        if (container.name == "phala-node"):
            phala["phalanode"] = container.status


    return phala
#print(getPhala("http://10.1.1.210"))
#print(str(getPhalaServices()))


