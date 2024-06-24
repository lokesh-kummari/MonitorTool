from flask import Flask, render_template, request, redirect, url_for
import subprocess
import platform
import socket
import os
from networkmap import generate_network_map

app = Flask(__name__)

def ping_test(ip_address):
    """Function to ping an IP address and check if it's reachable."""
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
    """Function to check if a device is connected and retrieve open ports."""
    try:
        online_status = ping_test(ip_address)
        if not online_status:
            return False, []

        open_ports = []
        for port in range(1, 1025):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1)
                result = s.connect_ex((ip_address, port))
                if result == 0:
                    open_ports.append(port)

        return True, open_ports
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False, []

def port_description(port):
    """Function to provide description for common ports."""
    port_dict = {
        20: "FTP Data - File Transfer Protocol for data transfer",
        21: "FTP Control - File Transfer Protocol for control (commands)",
        22: "SSH - Secure Shell for secure logins, file transfers (scp, sftp) and port forwarding",
        23: "Telnet - Unencrypted text communications",
        25: "SMTP - Simple Mail Transfer Protocol for email routing",
        53: "DNS - Domain Name System for resolving domain names to IP addresses",
        80: "HTTP - Hypertext Transfer Protocol for web traffic",
        110: "POP3 - Post Office Protocol for retrieving emails",
        443: "HTTPS - Hypertext Transfer Protocol Secure for secure web traffic",
    }
    return port_dict.get(port, "Unknown - No description available")

def check_connected_devices(ip_range):
    """Function to scan the network and retrieve connected devices with open ports."""
    devices = []
    port_descriptions = {}
    for i in range(1, 255):
        ip_address = f"{ip_range}.{i}"
        connected, open_ports = check_device_connection(ip_address)
        if connected:
            ports_info = [(port, port_description(port)) for port in open_ports]
            for port, desc in ports_info:
                if port not in port_descriptions:
                    port_descriptions[port] = desc
            devices.append({
                'ip': ip_address,
                'ports': ports_info
            })
    return devices, port_descriptions

@app.route('/')
def index():
    """Route for the index page."""
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_network():
    """Route to scan the network and display connected devices."""
    ip_range = '192.168.1'  # Fixed IP range for scanning
    devices, port_descriptions = check_connected_devices(ip_range)
    return render_template('results.html', devices=devices, port_descriptions=port_descriptions)

@app.route('/networkmap', methods=['POST'])
def network_map():
    """Route to generate and display the network map."""
    ip_range = "192.168.1.1/24"  # Adjust IP range as needed
    img_path = os.path.join('static', 'network_map.png')  # Path to save the network map image
    generate_network_map(ip_range, img_path)  # Generate the network map (ensure no threading issues here)
    return render_template('networkmap.html', img_path=img_path)  # Render template with the image path

if __name__ == "__main__":
    app.run(debug=True)
