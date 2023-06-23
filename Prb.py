import requests
import json
import re
from datetime import datetime


 #get prb peers from /ptp/discover in the prb monitor service at 10.2.3.2:3000. 
def getPrbLifecyclePeerId(baseUrl):
    url = baseUrl + ":3000/ptp/discover"
    r = requests.post(url)
    peers = r.json()
    # print(json.dumps(peers, indent=4, sort_keys=True))
    # print("Peer ID: " + peers["lifecycleManagers"][0]["peerId"])
    return peers["lifecycleManagers"][0]["peerId"]

# gets the peerid from getPrbLifecyclePeer, then using the peerid it gets the workers  from the ListWorker endpoint
def getPrbWorkers(baseUrl):
    result = []
    peerid = getPrbLifecyclePeerId(baseUrl)
    url = baseUrl + ":3000/ptp/proxy/" + peerid + "/GetWorkerStatus"
    print(url)
    r = requests.post(url)
    workers = r.json()

    for worker in workers["data"]["workerStates"]:
        worker.pop("minerInfoJson")
        worker['publicKey'] = "0x" + worker['publicKey']
        match = re.search(r'\[(.*?)\](.*)', worker["lastMessage"])
        if match:
            datetime_str = match.group(1)
            remainder_str = match.group(2)
            # Convert datetime string to datetime object
            dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S%z")
            # Convert datetime object to epoch time
            epoch_time = int(dt.timestamp())
            worker["lastMessage"] = remainder_str.lstrip()
            worker["lastMessageTime"] = epoch_time * 1000
            worker["worker"]["stake"] = int(worker["worker"]["stake"]) / 1000000000000
        result.append(worker)
        print(json.dumps(worker, indent=4, sort_keys=True))
    
    
    return result



#s = getPrbWorkers("http://10.2.3.2")
#print(json.dumps(s, indent=4, sort_keys=True))