#!/usr/bin/python3.9
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
    output = run_cmd(f"ip -o -f inet addr show | grep {ip}")
    if output:
        cidr = output.split()[3]
        return cidr.split('/')[1]
    return "N/A"

def get_system_disk():
    usage = psutil.disk_usage('/')
    return usage.total, usage.free

def main():
    os.system("clear")

    # Log file in user's home directory
    home_dir = os.path.expanduser("~")
    log_path = os.path.join(home_dir, "system_report.log")

    # Open file for writing
    with open(log_path, "a") as log:
        def log_print(text):
            print(text)
            log.write(text + "\n")

        log_print("===== System Report =====")
        # Get the current date and time
        log_print(f"Current date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Get and print hostname
        hostname = socket.gethostname()
        log_print(f"Host name: {hostname}")

        # Get and print domain suffix if it exists
        fqdn = socket.getfqdn()
        log_print(f"Domain suffix: {fqdn.replace(hostname+'.','') if fqdn != hostname else 'N/A'}")

        # Get and print IP information
        ip = run_cmd("hostname -I").split()[0] if run_cmd("hostname -I") else "N/A"
        log_print(f"IPv4 address: {ip}")
        log_print(f"Default gateway: {get_default_gateway()}")
        log_print(f"Network mask: {get_netmask(ip)}")

        # Get and print DNS server(s)
        dns_servers = get_dns_servers()
        log_print(f"Primary DNS server: {dns_servers[0]}")
        log_print(f"Secondary DNS server: {dns_servers[1] if len(dns_servers) > 1 else 'N/A'}")

        # Get and print OS name
        os_name = run_cmd("/etc/os-release | grep ^NAME= | cut -d= -f2").strip('"')
        log_print(f"Operating system name: {os_name}")

        # Get and print OS version
        os_version = run_cmd("cat /etc/os-release | grep ^VERSION= | cut -d= -f2").strip('"')
        log_print(f"Operating system version: {os_version}")

        # Get and print kernel version
        log_print(f"Kernel version: {platform.release()}")

        # Get disk size and information
        total_disk, free_disk = get_system_disk()
        log_print(f"System disk size: {total_disk // (1024**3)} GB")
        log_print(f"Available system disk space: {free_disk // (1024**3)} GB")

        # Get and print all cpu information
        log_print(f"CPU model: {run_cmd("lscpu | grep 'Model name' | awk -F: '{print $2}'").strip()}")
        log_print(f"Number of CPUs: {psutil.cpu_count(logical=True)}")
        log_print(f"Number of CPU cores: {psutil.cpu_count(logical=False)}")

        mem = psutil.virtual_memory()
        log_print(f"Total RAM: {mem.total // (1024**2)} MB")
        log_print(f"Available RAM: {mem.available // (1024**2)} MB")

    print(f"\nReport saved to: {log_path}")

if __name__ == "__main__":
    main()
