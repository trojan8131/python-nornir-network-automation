import subprocess

ips="""8.8.8.8
8.8.4.4"""

for ip in ips.splitlines():
    result = subprocess.run(['ping', '-c', '5', '-W', '1', ip], stdout=subprocess.PIPE)
    if result.returncode == 0:
        print(ip + ' is UP')
    else:
        print(ip + ' is DOWN')