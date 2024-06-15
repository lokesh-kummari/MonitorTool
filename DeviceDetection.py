import argparse
import subprocess
import platform
import socket
def ping_test(ip_address):
    # Determine the appropriate ping command based on the operating system
    if platform.system().lower() == "windows":
        command = ['ping', '-n', '1', '-w', '1000', ip_address]
    else:
        command = ['ping', '-c', '1', '-W', '1', ip_address]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def check_device_connection(ip_address):
    try:
        # Ping the device to check if it's online
        online_status = ping_test(ip_address)
        if not online_status:
            return False, []
        
        # Perform a port scan to gather information about open ports
        open_ports = []
        for port in range(1, 1025):  # Scan common ports
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1)
                result = s.connect_ex((ip_address, port))
                if result == 0:
                    open_ports.append(port)
        
        return True, open_ports
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False, []

def scan_network(ip_range):
    print("Scanning network for devices...\n")
    for i in range(1, 255):
        ip_address = f"{ip_range}.{i}"
        connected, open_ports = check_device_connection(ip_address)
        if connected:
            print(f"Device with IP address {ip_address} is connected to the LAN and has open ports: {open_ports}")
        else:
            print(f"Device with IP address {ip_address} is not connected to the LAN")

def main():
    parser = argparse.ArgumentParser(description="LAN Network Monitoring Tool")
    parser.add_argument("command", choices=["scan"], help="Command to execute")
    parser.add_argument("--range", "-r", help="IP range to scan (e.g., 192.168.1)")
    args = parser.parse_args()

    if args.command == "scan":
        if args.range:
            scan_network(args.range)
        else:
            print("Error: IP range not specified.")
            parser.print_help()

if __name__ == "__main__":
    main()