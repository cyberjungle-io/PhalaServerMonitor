
import subprocess

def SendPhalaUpdate():
    s = subprocess.call("phala stop", shell = True)
    s = subprocess.call("phala update", shell = True)
    

def SendPhalaRestart():
    s = subprocess.call("phala stop", shell = True)
    s = subprocess.call("phala start", shell = True)


def SendPhalaStart():
    s = subprocess.call("phala start", shell = True)

def SendPhalaStop():
    s = subprocess.call("phala stop", shell = True)

def UpdateMonitor():
    s = subprocess.call("./UpdateMonitor.sh", shell = True)