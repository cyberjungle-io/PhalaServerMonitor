
import subprocess

def SendPhalaUpdate():
    s = subprocess.call("docker-compose -f /home/oak/worker/docker-compose.yml down", shell = True)
    s = subprocess.call("docker-compose -f /home/oak/worker/docker-compose.yml pull", shell = True)
    s = subprocess.call("docker-compose -f /home/oak/worker/docker-compose.yml up -d", shell = True)
    

def SendPhalaRestart():
    s = subprocess.call("docker-compose -f /home/oak/worker/docker-compose.yml down", shell = True)
    s = subprocess.call("docker-compose -f /home/oak/worker/docker-compose.yml up -d", shell = True)
    


def SendPhalaStart():
    s = subprocess.call("docker-compose -f /home/oak/worker/docker-compose.yml up -d", shell = True)

def SendPhalaStop():
    s = subprocess.call("docker-compose -f /home/oak/worker/docker-compose.yml down", shell = True)





