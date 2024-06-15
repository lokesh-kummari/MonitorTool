import subprocess
import platform

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

def check_lan_status(ip_range):
    for i in range(1, 255):
        ip_address = f"{ip_range}.{i}"
        online_status = ping_test(ip_address)
        print(f"Device with IP address {ip_address} is {'online' if online_status else 'offline'}")

def main():
    ip_range = '192.168.1'  # Specify the first three octets of your LAN IP range
    check_lan_status(ip_range)

if __name__ == "__main__":
    main()