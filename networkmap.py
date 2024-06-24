import scapy.all as scapy
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use Agg backend

import matplotlib.pyplot as plt

from flask import Flask, send_file, request

app = Flask(__name__)

def scan_network(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        devices.append({
            'ip': element[1].psrc,
            'mac': element[1].hwsrc
        })
    
    return devices

def generate_network_map(ip_range, output_path):
    devices = scan_network(ip_range)
    if not devices:
        print("No devices found.")
        return

    G = nx.Graph()
    positions = {}

    for i, device in enumerate(devices):
        G.add_node(device['ip'], mac=device['mac'])
        positions[device['ip']] = (i, 0)

    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed
    nx.draw(G, pos=positions, with_labels=False, node_size=3000, node_color="lightblue", edge_color='gray', ax=ax)

    for node, (x, y) in positions.items():
        ax.text(x, y + 0.1, node, fontsize=10, ha='center', va='center', color='black', weight='bold')
        ax.text(x, y - 0.1, G.nodes[node]['mac'], fontsize=8, ha='center', va='center', color='gray')

    ax.set_title("Network Map")
    
    # Save the figure directly to file without displaying it
    fig.savefig(output_path)
    plt.close(fig)


@app.route('/generate_map', methods=['POST'])
def handle_generate_map():
    ip_range = request.form.get('ip_range')
    output_path = '/path/to/save/networkmap.png'  # Specify your desired output path

    generate_network_map(ip_range, output_path)

    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

