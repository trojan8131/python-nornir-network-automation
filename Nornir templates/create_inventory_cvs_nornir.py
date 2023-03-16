import datetime
import re
import os
import pprint
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_salt.plugins.tasks import netmiko_send_command_ps
from nornir_netmiko.tasks import netmiko_send_command
import csv

nr = InitNornir(config_file="config.yaml")




result = nr.run(task=napalm_get, getters=["facts"])
#print_result(result)
for device_name, task_result in result.items():
    if task_result.failed:
        print(f"{device_name} failed: {task_result.exception}")
    else:
        facts = task_result.result["facts"]
        print(f"Device {device_name} facts:")
        print(f"  Hostname: {facts['hostname']}")
        print(f"  Model: {facts['model']}")
        print(f"  Vendor: {facts['vendor']}")
        print(f"  Serial Number: {facts['serial_number']}")
        print(f"  OS Version: {facts['os_version']}")

# Open CSV file for writing
with open("device_facts.csv", "w", newline="") as csvfile:
    # Define CSV writer object and write header row
    fieldnames = ["hostname", "model", "vendor", "serial_number", "os_version"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Write data rows
    for device_name, task_result in result.items():
        if task_result.failed:
            print(f"{device_name} failed: {task_result.exception}")
        else:
            facts = task_result.result["facts"]
            pattern = re.compile(r"Version\s(.+),")
            match = pattern.search(facts["os_version"])
            if match:
                version = match.group(1)
                #print(version)
                writer.writerow({
                    "hostname": facts["hostname"],
                    "model": facts["model"],
                    "vendor": facts["vendor"],
                    "serial_number": facts["serial_number"],
                    "os_version": version
                })
            else:
                writer.writerow({
                    "hostname": facts["hostname"],
                    "model": facts["model"],
                    "vendor": facts["vendor"],
                    "serial_number": facts["serial_number"],
                    "os_version": facts["os_version"]
                })

