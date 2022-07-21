import os
import psutil
import requests
import json
import platform
import time
import socket

def getIpAddress():
    return socket.gethostbyname(socket.gethostname())  

# get the total number of cores.
def getCores():
    return round(os.cpu_count())


# gets the hightest core temperature and critical temperature
def getCpuTemp():
    temp = 0
    maxtemp = 0
    criticaltemp = 0
    for tmp in psutil.sensors_temperatures()["coretemp"]:
           #	print(tmp[1])
        if tmp[1] > temp:
            temp = tmp[1]
        if tmp[3] > criticaltemp:
            criticaltemp = tmp[3]

    return temp, criticaltemp

# Get the total cpu usage as a percentage
def getCpuPercent():
    cpu_load = psutil.cpu_percent(interval=0.5)
    return round(cpu_load)

# Get the total and used ram
def getRAM():
    total = psutil.virtual_memory().total
    used = int(psutil.virtual_memory().total - psutil.virtual_memory().available)
    return used , total

def getHostName():
    return platform.node()

def getLinuxData():
    temp, ctemp = getCpuTemp()
    used, totalram = getRAM()
    result = {
        "cores": getCores(),
        "CPU_Temp": temp,
        "Critical_Temp": ctemp,
        "CPULoad": getCpuPercent(),
        "total_ram": totalram,
        "used_ram": used,
        "ip_address": getIpAddress()
    }
    return result