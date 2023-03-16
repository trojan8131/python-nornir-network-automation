import datetime
import re
import os
import pprint
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_salt.plugins.tasks import netmiko_send_command_ps
from nornir_netmiko.tasks import netmiko_send_command
from nornir_netmiko.tasks import netmiko_send_config
from termcolor import colored
from tabulate import tabulate
import time
from nornir.core.filter import F

nr = InitNornir(config_file="config.yaml")


def filter_func(host):
    #print(host.data["country"])
    return "IT" in host.data["country"]

def filter_func2(host):
    #print(host.data["country"])
    return "SW-" in host.data["hostname"]

def getter(task):
    task.run(task=napalm_get, getters=["facts"])
    print_result(task)

filtered_hosts = nr.filter(filter_func)
sklepy = filtered_hosts.filter(filter_func2)


sklepy = sklepy.filter(F(name__contains="WRO"))	
sklepy = nr.filter(F(groups__all=["switch"]))	



print(len(filtered_hosts.inventory.hosts))
pprint.pprint(sklepy.inventory.hosts)

temp=sklepy.run(task=getter)
print_result(temp)


