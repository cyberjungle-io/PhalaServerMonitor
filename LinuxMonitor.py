import os
import psutil
import requests
import json
import platform
import time
import socket
import docker

def getDockerList():
    client = docker.from_env()

    instances = []

    for container in client.containers.list():
        tinst = {
            "name": container.name,
            "status": container.status
        }
        
        instances.append(tinst)
    return instances
import subprocess

def get_docker_logs(docker_compose_path,service_name,num_logs):
    

    # Build the Docker command to retrieve logs
    docker_command = f'docker-compose -f {docker_compose_path} logs --tail={num_logs} {service_name}'

    try:
        # Execute the Docker command and capture the output
        logs = subprocess.check_output(docker_command, shell=True, universal_newlines=True)
        
        # Split the logs by newline character
        log_lines = logs.split('\n')

        # Create a list to store log entries
        log_entries = []
        
        # Process each log line
        for line in log_lines:
            # Skip empty lines
            if line.strip() == '':
                continue
            
            # Split the log line into timestamp and message
            timestamp, message = line.split(' ', 1)
            
            # Create a dictionary for the log entry
            log_entry = {'timestamp': timestamp, 'message': message}
            
            # Add the log entry to the list
            log_entries.append(log_entry)

        # Convert the log entries to JSON format
        json_logs = json.dumps(log_entries, indent=4)
        
        return json_logs
    except subprocess.CalledProcessError as e:
        print(f'Error retrieving Docker logs: {e}')
        return None

def getIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

# get the total number of cores.
def getCores():
    return round(os.cpu_count())


# gets the hightest core temperature and critical temperature
def getCpuTemp():

    temp = 0
    maxtemp = 0
    criticaltemp = 0
    try:
        for tmp in psutil.sensors_temperatures()["coretemp"]:
            #	print(tmp[1])
            if tmp[1] > temp:
                temp = tmp[1]
            if tmp[3] > criticaltemp:
                criticaltemp = tmp[3]
    except:
        temp = 0
        maxtemp = 0
        criticaltemp = 0

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