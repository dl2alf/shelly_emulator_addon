from flask import Flask, jsonify
import threading
import time
import requests
import os

app = Flask(__name__)

TASMOTA_IP = os.environ.get("TASMOTA_IP", "192.168.1.50")
TASMOTA_API_URL = f"http://{TASMOTA_IP}/cm?cmnd=Status%208"

latest_data = {
    "power": 0.0,
    "voltage": 230.0,
    "total": 0.0
}

def fetch_real_data():
    try:
        response = requests.get(TASMOTA_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        haus = data.get("StatusSNS", {}).get("Haus", {})

        return {
            "power": float(haus.get("power_in", 0)),
            "voltage": 230.0,
            "total": float(haus.get("energy_in", 0)) * 1000
        }

    except Exception as e:
        print(f"[ERROR] Failed to fetch Tasmota data: {e}")
        return latest_data

def update_loop():
    global latest_data
    while True:
        latest_data = fetch_real_data()
        print(f"[INFO] Updated data: {latest_data}")
        time.sleep(10)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "wifi_sta": {"connected": True},
        "mac": "DE:AD:BE:EF:12:34",
        "meters": [{
            "power": latest_data["power"],
            "total": latest_data["total"],
            "voltage": latest_data["voltage"],
            "is_valid": True
        }],
        "update": {"has_update": False},
        "ram_total": 51200,
        "ram_free": 25000,
        "uptime": int(time.time()),
        "fw_ver": "1.12.1"
    })

@app.route('/settings', methods=['GET'])
def settings():
    return jsonify({
        "device": {"mac": "DE:AD:BE:EF:12:34"},
        "name": "Emulated Shelly",
        "wifi_sta": {"ssid": "EmulatorWiFi"}
    })

if __name__ == '__main__':
    threading.Thread(target=update_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=80)
