import subprocess
import json
import socket
import os
import requests

# Function to validate a URL
def validate_url(url):
    return url.startswith('http://') or url.startswith('https://')

# Function to validate the monitor type
def validate_monitor_type(monitor_type):
    valid_types = ['solo', 'prb', 'prbworker', 'phalanode']
    return monitor_type in valid_types

# Function to validate the interval
def validate_interval(interval):
    try:
        interval = int(interval)
        return interval > 0
    except ValueError:
        return False

# Function to get the default value for monitor URL
def get_default_monitor_url():
    return 'https://phalaserver.cyberjungle.io'

# Function to get the default value for host name
def get_default_host_name():
    return socket.gethostname()

# Check if config.json exists and load existing configuration if it does
config = {}
if os.path.exists('config.json'):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

# Prompt for monitor type
monitor_type = input("Enter the monitor type (solo/prb/prbworker,phalanode) (default: {}): ".format(config.get('monitorType', ''))) or config.get('monitorType')

while monitor_type is None or not validate_monitor_type(monitor_type):
    print("Invalid monitor type. Please enter one of the following: solo, prb, prbworker, phalanode")
    monitor_type = input("Enter the monitor type (solo/prb/prbworker/phalanode) (default: {}): ".format(config.get('monitorType', ''))) or config.get('monitorType')

# Prompt for service name
service_name = input("Enter the service name (default: {}): ".format(config.get('serviceName', get_default_host_name()))) or config.get('serviceName', get_default_host_name())

# Prompt for host name
host_name = input("Enter the host name (default: {}): ".format(config.get('hostName', get_default_host_name()))) or config.get('hostName', get_default_host_name())

# Prompt for monitor URL
monitor_url = input("Enter the monitor URL (default: {}): ".format(config.get('monitorUrl', get_default_monitor_url()))) or config.get('monitorUrl', get_default_monitor_url())
while not validate_url(monitor_url):
    print("Invalid monitor URL. Please enter a valid URL starting with 'http://' or 'https://'")
    monitor_url = input("Enter the monitor URL (default: {}): ".format(config.get('monitorUrl', get_default_monitor_url()))) or config.get('monitorUrl', get_default_monitor_url())

# Prompt for monitor key and validate
monitor_key = input("Enter the monitor key (default: {}): ".format(config.get('monitorKey', ''))) or config.get('monitorKey')

if monitor_key:
    validation_url = monitor_url.rstrip('/') + '/servermonitor/checkMonitorKey'
    payload = {
        'monitorKey': monitor_key
    }
    try:
        response = requests.post(validation_url, json=payload)
        response.raise_for_status()
        response_data = response.json()
        is_valid_key = response_data.get('isValidKey', False)

        while not is_valid_key:
            print("Invalid monitor key. Please enter a valid key.")
            monitor_key = input("Enter the monitor key (default: {}): ".format(config.get('monitorKey', ''))) or config.get('monitorKey')
            payload['monitorKey'] = monitor_key
            response = requests.post(validation_url, json=payload)
            response.raise_for_status()
            response_data = response.json()
            is_valid_key = response_data.get('isValidKey', False)

    except requests.exceptions.RequestException as e:
        print("Error occurred while validating monitor key:", e)
        monitor_key = None

# Prompt for interval
interval = input("Enter the interval in seconds (default: 60): ") or str(config.get('interval', 60))
while not validate_interval(interval):
    print("Invalid interval. Please enter a positive integer value.")
    interval = input("Enter the interval in seconds (default: 60): ") or str(config.get('interval', 60))
node_base_url = input("Enter the node base URL (default: {}): ".format(config.get('nodeBaseUrl', 'http://localhost'))) or config.get('nodeBaseUrl', 'http://localhost')
   
# Create the configuration dictionary
config = {
    "monitorType": monitor_type,
    "serviceName": service_name,
    "hostName": host_name,
    "monitorUrl": monitor_url,
    "monitorKey": monitor_key,
    "nodeBaseUrl": node_base_url,
    "interval": int(interval)
}

# Additional data collection for solo monitor type


# Save the configuration to a JSON file
with open('config.json', 'w') as config_file:
    json.dump(config, config_file, indent=4)

print("Configuration saved to config.json.")

# Prompt for auto-start option
auto_start = input("Do you want to have this service auto start? (Y/N) (default: Y): ").lower() or 'y'
if auto_start == 'y':
    # Execute the install_autoboot.sh script
    subprocess.call('./install_autoboot.sh', shell = True)
