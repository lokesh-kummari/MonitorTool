import psutil
import time

def get_network_stats(previous_stats):
    net_io = psutil.net_io_counters(pernic=True)
    usage_stats = {}

    for interface, stats in net_io.items():
        if interface in previous_stats:
            # Use dictionary access notation for bytes_sent and bytes_recv
            sent = stats.bytes_sent - previous_stats[interface]['bytes_sent']
            recv = stats.bytes_recv - previous_stats[interface]['bytes_recv']

            usage_stats[interface] = {
                'bytes_sent': stats.bytes_sent,
                'bytes_recv': stats.bytes_recv,
                'bytes_sent_sec': sent,
                'bytes_recv_sec': recv
            }
        else:
            # Initialize usage_stats for new interface
            usage_stats[interface] = {
                'bytes_sent': stats.bytes_sent,
                'bytes_recv': stats.bytes_recv,
                'bytes_sent_sec': 0,
                'bytes_recv_sec': 0
            }

    return usage_stats

def display_network_stats(stats):
    for interface, data in stats.items():
        print(f"Interface: {interface}")
        print(f"  Total Bytes Sent: {data['bytes_sent']} bytes")
        print(f"  Total Bytes Received: {data['bytes_recv']} bytes")
        print(f"  Bandwidth Usage (Sent): {data['bytes_sent_sec']} bytes/sec")
        print(f"  Bandwidth Usage (Received): {data['bytes_recv_sec']} bytes/sec")
        print("-" * 40)

if __name__ == "__main__":
    previous_stats = {}

    while True:
        current_stats = get_network_stats(previous_stats)
        display_network_stats(current_stats)
        # Update previous_stats with the current stats for the next iteration
        previous_stats = {interface: {
            'bytes_sent': data['bytes_sent'],
            'bytes_recv': data['bytes_recv']
        } for interface, data in current_stats.items()}
        time.sleep(5)  # Sleep for 5 seconds before printing stats again
