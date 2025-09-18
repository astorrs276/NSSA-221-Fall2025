#!/usr/bin/python3.9
import os
import subprocess

# Alexander Storrs
# 9/17/2025

# Function to print all of the command options
def print_options():
    print('''
1. Display the default gateway
2. Test local connectivity
3. Test remote connectivity
4. Test DNS resolution
5. Exit/quit the script''')

# Check for the default gateway dynamically
# Uses `ip route` to get the gateway with `grep` and `awk` to parse it from the other info
def default_gateway():
    command = "ip route | grep '^default' | awk '{print $3}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    gateway = result.stdout.strip()
    return gateway

# Checks the local connection by pinging localhost
def local_connection():
    command = ["ping", "-c", "2", "127.0.0.1"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return "FAILED"

# Checks the remote connection by pinging RIT's DNS server
def remote_connection():
    command = ["ping", "-c", "2", "129.21.3.17"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return "FAILED"

# Checks the DNS connection by pinging Google
def dns_connection():
    command = ["ping", "-c", "2", "www.google.com"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return "FAILED"

# Main function to get the user's action and run everything accordingly
def main():
    os.system("clear")
    while True:
        print_options()
        choice = input(">> ")
        if choice == "1":
            os.system("clear")
            print("You selected option 1.")
            gateway = default_gateway()
            print("Default gateway:", gateway)
        elif choice == "2":
            os.system("clear")
            print("You selected option 2.")
            print("Testing Local connection:")
            print(local_connection())
        elif choice == "3":
            os.system("clear")
            print("You selected option 3.")
            print("Testing remote connection:")
            print(remote_connection())
        elif choice == "4":
            os.system("clear")
            print("You selected option 4.")
            print("Testing DNS:")
            print(dns_connection())
        elif choice == "5":
            print("Goodbye")
            break
        else:
            os.system("clear")
            print("Invalid input")

if __name__ == '__main__':
    main()
