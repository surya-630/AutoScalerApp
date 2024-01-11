# AutoScalerApp

## Overview

This script implements an auto-scaler for adjusting the number of replicas of an application based on CPU utilization metrics. The application, provided by the target application, emulates CPU usage and exposes JSON/REST APIs for monitoring and adjusting the number of replicas.

## Features

- Monitors CPU utilization of the target application.
- Adjust the number of replicas to maintain an average CPU usage of 80%.
- Handles real-life condition errors and logs it to **autoscaler.log**.

## Requirements

- Python (version 3.x recommended)
- Required Python packages: `requests`

```bash
pip install requests

**Configuration**

**Set the base_url variable in the script to the URL of the Vimeo application.**
base_url = "http://target-app-url"

**Adjust the target_cpu and threshold values based on your scaling requirements.**
auto_scaler = AutoScaler(base_url, target_cpu=0.80, threshold=0.05)

**Logging**
The script logs messages to a rotating log file ("autoscaler.log") with a maximum size of 10 MB and keeps 3 backup files.

**Usage**

**Run the script:**

**python autoscaler_script.py**
The script will run infinitely, adjusting replicas based on CPU utilization every 60 seconds. Terminate the script using Ctrl + C (in Windows and Linux) & Cmd + C (in Mac).
