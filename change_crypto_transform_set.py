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
import argparse


info=[]
def unlock_crypto_all(task):
    result = task.run(task=netmiko_send_command, command_string=f"show run | i crypto map c_map ")
    for line in result.result.splitlines():
        if "ipsec-isakmp" in line:
            #commands=[line,"set transform-set ts-esp-aes256-sha256"]
            commands=[line,"set transform-set ts-crypto"]
            #print(line)
            r = task.run(task=netmiko_send_config, config_commands=commands)
            print_result(r)




def check_up(task):
    global sh_crypto_session_brief
    r = task.run(task=netmiko_send_command, command_string=f"sh crypto session brief | in UA")
    #print_result(r)
    #print(r.result)
    sh_crypto_session_brief=sh_crypto_session_brief+r.result
    #print(sh_crypto_session_brief)


nr = InitNornir(config_file="./config.yaml")
unlock = nr.run(task=unlock_crypto_all)

print(tabulate(info))
