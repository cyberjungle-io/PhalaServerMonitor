# from turtle import clear
import requests
import json

def getKhala():
    baseurl = "https://khala.api.subscan.io"

    uri = baseurl + "/api/scan/blocks"
    srch = {  
        "row": 1,
        "page": 0
    }
    try:
        response = requests.post(uri,json=srch,timeout=45)
        data = response.json()
        if response.status_code == 200: 
            khala = data["data"]["blocks"][0]["block_num"]
        else:
            return 0

    except:
        return 0
    #print(json.dumps(data["data"]["blocks"][1]["block_num"],indent=4))
    return khala



def getKusama():
    baseurl = "https://kusama.api.subscan.io"

    uri = baseurl + "/api/scan/blocks"
    srch = {  
        "row": 1,
        "page": 0
    }
    try:
        response = requests.post(uri,json=srch,timeout=45)
        data = response.json()
        if response.status_code == 200:
            kusama = data["data"]["blocks"][0]["block_num"]
        else:
            return 0
    except requests.HTTPError as e:
        print(e)
        return 0
    #print(json.dumps(data["data"]["blocks"][1]["block_num"],indent=4))
    return kusama
 


def getAccountBalance(address):
    baseurl = "https://khala.api.subscan.io"
    bal = 0
    baloc = 0
    uri = baseurl + "/api/v2/scan/search"
    srch = {  
        
        "key": address
    }
    try:
        response = requests.post(uri,json=srch,timeout=45)
        data = response.json()
        bal = data["data"]["account"]["balance"]
        baloc  = data["data"]["account"]["balance_lock"]

     #   khala = data["data"]["blocks"][0]["block_num"]
    except:
        return -1 , -1
    #print(json.dumps(data["data"]["account"]["balance"],indent=4))
    #print(json.dumps(data["data"]["account"]["balance_lock"],indent=4))
    return bal, baloc


#bal,balock = getAccountBalance("42mKhRT6T3huTi52b7F18ZFnyQPFub5fRvPQ4U5BP2Cvu7LJ")
#print("Balance: " + str(bal) + "  locked: " + str(balock))