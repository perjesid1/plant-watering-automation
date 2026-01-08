# ==========================================
# MQTT TESZT KLIENS (PC / laptop oldalon)
# ==========================================
# Ez a program NEM a mikrokontrolleren fut,
# hanem normál Python környezetben.
#
# Célja:
# - az MQTT broker (HiveMQ Cloud) tesztelése
# - a Node-RED dashboard kipróbálása
# - hardver nélküli fejlesztés támogatása
# ==========================================
import time
import json
import paho.mqtt.client as mqtt
import config

# -------------------------------
# Titkos adatok betöltése
# -------------------------------
# A secrets.py tartalmazza az MQTT
# felhasználónevet és jelszót
try:
    import secrets
except ImportError:
    secrets = None

# ================================
# MQTT kapcsolat létrehozása
# ================================
def connect_mqtt():
    if not secrets:
        print("No secrets.py found, cannot connect")
        return None

    # MQTT kliens létrehozása egyedi Client ID-val
    client = mqtt.Client(client_id=config.MQTT_CLIENT_ID)
    client.username_pw_set(secrets.MQTT_USERNAME, secrets.MQTT_PASSWORD)

    # TLS engedélyezése (HiveMQ Cloud követelmény)
    if config.MQTT_USE_TLS:
        client.tls_set()  # alap TLS beállítás

    # Csatlakozás a brokerhez
    client.connect(config.MQTT_BROKER, config.MQTT_PORT)
    print("Connected to HiveMQ broker")
    return client

# ================================
# MQTT üzenet küldése
# ================================
def mqtt_publish_status(client, payload: dict):
    topic = f"{config.MQTT_TOPIC_BASE}/status"

    # Python dictionary → JSON string
    client.publish(topic, json.dumps(payload))
    print(f"Published to {topic}: {payload}")

# ================================
# Fő tesztprogram
# ================================
def main():
    client = connect_mqtt()
    if not client:
        return

    # 5 darab tesztüzenet küldése
    for i in range(5):
        payload = {
            "moisture": 30 + i*5,
            "light": "Dark" if i % 2 == 0 else "Bright",
            "needs_watering": i % 2 == 0,
            "timestamp": int(time.time())
        }
        mqtt_publish_status(client, payload)
        time.sleep(5)

    # Kapcsolat bontása
    client.disconnect()
    print("MQTT test finished")

# ================================
# Program indítása
# ================================
if __name__ == "__main__":
    main()
