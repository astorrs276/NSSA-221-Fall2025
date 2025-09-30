#!/usr/bin/python3.9
'''
import os
import subprocess

# Alexander Storrs
# 9/30/2025

def main():
    os.system("clear")


if __name__ == "__main__":
    main()
'''

import os
import socket
import subprocess
import platform
import psutil
import datetime
import re

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except subprocess.CalledProcessError:
        return "N/A"

def get_dns_servers():
    dns = []
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    dns.append(line.split()[1])
    except FileNotFoundError:
        pass
    return dns if dns else ["N/A"]

def get_default_gateway():
    route = run_cmd("ip route show default")
    match = re.search(r"default via ([0-9.]+)", route)
    return match.group(1) if match else "N/A"

def get_netmask(ip):
    # Find netmask for the given IP
    output = run_cmd("ip -o -f inet addr show")
    for line in output.splitlines():
        if ip in line:
            match = re.search(r"/(\d+)", line)
            if match:
                prefix = int(match.group(1))
                mask = (0xffffffff >> (32 - prefix)) << (32 - prefix)
                return ".".join([str((mask >> (i * 8)) & 0xff) for i in [3, 2, 1, 0]])
    return "N/A"

def get_system_disk():
    usage = psutil.disk_usage('/')
    return usage.total, usage.free

def main():
    print("===== System Report =====")
    print(f"Current date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    hostname = socket.gethostname()
    fqdn = socket.getfqdn()
    ip = run_cmd("hostname -I").split()[0] if run_cmd("hostname -I") else "N/A"

    print(f"Host name: {hostname}")
    print(f"Domain suffix: {fqdn.replace(hostname+'.','') if fqdn != hostname else 'N/A'}")
    print(f"IPv4 address: {ip}")
    print(f"Default gateway: {get_default_gateway()}")
    print(f"Network mask: {get_netmask(ip)}")
    
    dns_servers = get_dns_servers()
    print(f"Primary DNS server: {dns_servers[0]}")
    print(f"Secondary DNS server: {dns_servers[1] if len(dns_servers) > 1 else 'N/A'}")

    # OS info
    os_name = run_cmd("cat /etc/os-release | grep ^NAME= | cut -d= -f2").strip('"')
    os_version = run_cmd("cat /etc/os-release | grep ^VERSION= | cut -d= -f2").strip('"')
    kernel_version = platform.release()

    print(f"Operating system name: {os_name}")
    print(f"Operating system version: {os_version}")
    print(f"Kernel version: {kernel_version}")

    # Disk info
    total_disk, free_disk = get_system_disk()
    print(f"System disk size: {total_disk // (1024**3)} GB")
    print(f"Available system disk space: {free_disk // (1024**3)} GB")

    # CPU info
    cpu_model = run_cmd("lscpu | grep 'Model name' | awk -F: '{print $2}'").strip()
    cpu_count = psutil.cpu_count(logical=True)
    cpu_cores = psutil.cpu_count(logical=False)
    print(f"CPU model: {cpu_model}")
    print(f"Number of CPUs: {cpu_count}")
    print(f"Number of CPU cores: {cpu_cores}")

    # Memory
    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total // (1024**2)} MB")
    print(f"Available RAM: {mem.available // (1024**2)} MB")

if __name__ == "__main__":
    main()
