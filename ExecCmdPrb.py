
import subprocess

def StopLifecycle():
    s = subprocess.call("docker-compose -f /home/oak/lifecycle/docker-compose.yml down", shell = True)
    
def StartLifecycle():
    s = subprocess.call("docker-compose -f /home/oak/lifecycle/docker-compose.yml up -d", shell = True)
     
def RestartLifecycle():
    s = subprocess.call("docker-compose -f /home/oak/lifecycle/docker-compose.yml down", shell = True)
    s = subprocess.call("docker-compose -f /home/oak/lifecycle/docker-compose.yml up -d", shell = True)



def StopDataProvider():
    s = subprocess.call("docker-compose -f /home/oak/provider/docker-compose.yml down", shell = True)
    
def StartDataProvider():
    s = subprocess.call("docker-compose -f /home/oak/provider/docker-compose.yml up -d", shell = True)
     
def RestartDataProvider():
    s = subprocess.call("docker-compose -f /home/oak/provider/docker-compose.yml down", shell = True)
    s = subprocess.call("docker-compose -f /home/oak/provider/docker-compose.yml up -d", shell = True)


def StopNode():
    s = subprocess.call("docker-compose -f /home/oak/node/docker-compose.yml down", shell = True)
    
def StartNode():
    s = subprocess.call("docker-compose -f /home/oak/node/docker-compose.yml up -d", shell = True)
     
def RestartNode():
    s = subprocess.call("docker-compose -f /home/oak/node/docker-compose.yml down", shell = True)
    s = subprocess.call("docker-compose -f /home/oak/node/docker-compose.yml up -d", shell = True)




def StopPrb():
    StopDataProvider()
    StopLifecycle()
    StopNode()

def StartPrb():
    StartNode()
    StartDataProvider()
    StartLifecycle()

def RestartPrb():
    StopPrb()
    StartPrb()



def StartDockerCompose(pth):
    s = subprocess.call("docker-compose -f " + pth + " up -d", shell = True)

def StopDockerCompose(pth):
    s = subprocess.call("docker-compose -f " + pth + " down", shell = True)
    

