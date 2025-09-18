#!/usr/bin/python3.9
import os
import subprocess

def print_options():
    print('''
1. Display the default gateway
2. Test local connectivity
3. Test remote connectivity
4. Test DNS resolution
5. Exit/quit the script''')

def default_gateway():
    command = "ip route | grep '^default' | awk '{print $3}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    gateway = result.stdout.strip()
    return gateway

def local_connection():
    command = ["ping", "-c", "2", "127.0.0.1"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return "FAILED"

def remote_connection():
    command = ["ping", "-c", "2", "8.8.8.8"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return "FAILED"

def dns_connection():
    command = ["ping", "-c", "2", "www.google.com"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return "FAILED"

def main():
    while True:
        print_options()
        choice = input(">> ")
        if choice == "1":
            gateway = default_gateway()
            print("Default gateway:", gateway)
        elif choice == "2":
            print("Testing Local connection:")
            print(local_connection())
        elif choice == "3":
            print("Testing remote connection:")
            print(remote_connection())
        elif choice == "4":
            print("Testing DNS:")
            print(dns_connection())
        elif choice == "5":
            print("Goodbye")
            break
        else:
            print("Invalid input")

if __name__ == '__main__':
    main()
