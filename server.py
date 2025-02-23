import os
import re
import socket
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_hostname(ip):
    """Intenta obtener el hostname de una IP"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Desconocido"

def scan_network():
    """Escanea la red usando 'arp -a' para obtener dispositivos conectados"""
    devices = []
    
    # Ejecuta el comando arp -a y captura la salida
    output = os.popen("arp -a").read()
    
    # Expresión regular para extraer las IPs y MACs
    matches = re.findall(r"(\d+\.\d+\.\d+\.\d+)\s+([\w-]+)", output)

    for ip, mac in matches:
        if mac != "ff-ff-ff-ff-ff-ff" and mac != "00-00-00-00-00-00":
            hostname = get_hostname(ip)
            devices.append({
                "ip": ip,
                "mac": mac,
                "hostname": hostname
            })

    return devices

@app.route('/scan', methods=['GET'])
def scan():
    devices = scan_network()
    return jsonify(devices)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
