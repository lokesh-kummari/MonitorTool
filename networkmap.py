import scapy.all as scapy
import networkx as nx
import matplotlib.pyplot as plt

def scan_network(ip_range):
    """Scan the network to find devices and their MAC addresses."""
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

def draw_network_map(devices):
    """Draw a network map using networkx and matplotlib."""
    G = nx.Graph()
    positions = {}
    
    # Add nodes and their attributes
    for i, device in enumerate(devices):
        G.add_node(device['ip'], mac=device['mac'])
        # Position nodes with a vertical offset to avoid overlap
        positions[device['ip']] = (i, 0)  # Position nodes along the x-axis

    # Draw nodes
    nx.draw(G, pos=positions, with_labels=False, node_size=3000, node_color="lightblue", edge_color='gray')
    
    # Annotate nodes with IP addresses and MAC addresses
    for node, (x, y) in positions.items():
        plt.text(x, y + 0.1, node, fontsize=10, ha='center', va='center', color='black', weight='bold')  # IP above node
        plt.text(x, y - 0.1, G.nodes[node]['mac'], fontsize=8, ha='center', va='center', color='gray')  # MAC below node
    
    plt.title("Network Map")
    plt.show()

if __name__ == "__main__":
    ip_range = "192.168.1.1/24"  # Change this to your network's IP range
    devices = scan_network(ip_range)
    if devices:
        draw_network_map(devices)
    else:
        print("No devices found. Please check your network settings and try again.")
