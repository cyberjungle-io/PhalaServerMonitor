#!/bin/bash

# Read the config.json file
config_file="config.json"
monitor_type=$(jq -r '.monitorType' "$config_file")

# Check the monitorType value and run the appropriate script using nohup
if [ "$monitor_type" = "solo" ]; then
    nohup python3 solomonitor.py &
elif [ "$monitor_type" = "prbworker" ]; then
    nohup python3 workermonitor.py &
elif [ "$monitor_type" = "prb" ]; then
    nohup python3 prbmonitor.py &
elif [ "$monitor_type" = "phalanode" ]; then
    nohup python3 phalanodemonitor.py &
else
    echo "Invalid monitorType value in config.json"
    exit 1
fi
