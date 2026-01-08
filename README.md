# plant-watering-automation

## Projekt célja

**A növény öntözésének automatizálása** úgy, hogy csak akkor locsoljon, ha a talaj nedvessége egy küszöbérték alá esik, és az öntözések között minimum 1 óra teljen el.

**Funkciók:**
- Kapacitív talajnedvesség-mérés (ADC)  
- Fényviszonyok érzékelése LDR-rel  
- Ví zpumpa vezérlése relémodullal  
- OLED-es helyi kijelzés  
- MQTT-n keresztüli adatszolgáltatás egy **Node-RED alapú webes dashboard** felé  

## Csapat tagjai és feladatkiosztás

**Perjési Dániel** – *Hardware design & Embedded software*  
Szenzorok, relé és vízpumpa bekötése az ESP32-höz, tápellátás, breadboard/prototípus összeállítása. `boot.py`, `config.py`, `main.py` és az OLED‑kezelés megírása MicroPythonban, mélységi alvás (deep sleep) logika és öntözési algoritmus  

**Gyarmati Gábor** – *Cloud & dashboard*  
HiveMQ Cloud MQTT broker beállítása, Node‑RED flow elkészítése, dashboard (Moisture %, Light, Thirsty státusz) kialakítása  

**Spacsek-Kovács Kinga** – *Documentation*  
README, BOM, lábkiosztás, fotók, projekt dokumentáció


**Hardveres BOM:**

| Alkatrész neve / leírás                                      | Gyártói cikkszám | Kategória                          | Mennyiség | Ref  |
|--------------------------------------------------------------|------------------|------------------------------------|-----------|------|
| ESP32-WROOM-32D fejlesztő lap WiFi és bluetooth              | IOT215           | Fejlesztőkártyák WiFi/Bluetooth    | 1         | U1   |
| Kapacitív talajnedvesség-érzékelő (VST581)                   | VST581           | Talajnedvesség szenzor             | 1         | U2   |
| Kis vízszivattyú - Vertikális (OST8502)                      | OST8502          | DC vízpumpa                        | 1         | M1   |
| Relémodul 1 csatorna H/L áthidalóval - 5 V (REL9884)         | REL9884          | 1 csatornás DC-DC relé             | 1         | K1   |
| Terminál adapter ESP32 38-tűs (SHI631)                       | SHI631           | Bővítőmodulok                      | 1         | AD1  |
| Tömlő vízszivattyúkhoz 6.5 mm (OST871)                       | OST871           | Szerelési anyag                    | 1         | T1   |
| Wago terminál PCT-415 1*5 (KAB2265)                          | KAB2265          | Sorkapcsok                         | 1         | W1   |
| Fotorezisztor (LDR)                                          | LDR-GL5528       | Fényérzékelő                       | 1         | R1   |
| Ellenállás 10 kΩ                                             |   RES-10K        | Passzív elem (LDR osztóhoz)        | 1         | R2   |
| Kijelző                                                      |                  |                                    | 1         | S1   |
| Power Adapter                                                |                  |                                    | 1         | PA1  |

A BOM a techfun.hu áruházból származó pontos cikkszámokat tartalmazza, amelyekkel a projekt prototípusa készült; a relémodul H/L jumperrel támogatja mind HIGH, mind LOW trigger módot.


**Szoftveres BOM**

| Komponens / Szolgáltató | Verzió / Típus | Cél / Megjegyzés |
|-------------------------|----------------|------------------|
| MicroPython firmware    | ESP32 stable   | Futtatókörnyezet |
| HiveMQ Cloud*           | TLS/8883       | MQTT broker      |
| Thonny IDE              | 4.1.7          | ESP32 programozás|
| Visual Studio Code      | -              | Kód szerkesztés  |
| Python                  | 3.x            | mqtt_test.py     |

MicroPython modulok:
- `machine` (Pin/ADC/I2C/RTC)
- `time`, `network`, `json`, `math`

**Könyvtárak:**
python
- ssd1306.py      # SSD1306 OLED driver (128x32, I2C)
- umqtt.simple    # MQTT kliens HiveMQ Cloudhoz (TLS)
- paho-mqtt       # PC-s tesztkliens (mqtt_test.py)

**Fejlesztői eszközök:**
- Thonny 4.1.7 – MicroPython fájlok feltöltése ESP32-re, soros monitor
- VS Code –  Kód szerkesztés, GitHub integráció
- Node-RED – Webes dashboard (MQTT-in → JSON → gauge/text widgetek)

## Használt források 

- **[MicroPython Kapacitív Talajnedvesség Szenzor](https://github.com/ashleywm/micropython-capacitive-soil-moisture-sensor/blob/master/src/CSMS.py)**  
  Talajnedvesség-szenzor kezelés, kalibráció inspirációja (VST581 szenzorhoz)
  
- **[MicroPython - LDR/Fotorezisztor olvasása](https://www.donskytech.com/micropython-read-ldr-or-photoresistor/)**  
  Fotorezisztor (LDR) GPIO olvasása, fényviszony állapot meghatározása


**Lábkiosztás táblázat:**

| Alkatrész          | ESP32 GPIO | Típus  | Cikkszám |
|--------------------|------------|--------|----------|
| **Relémodul IN**   | **GPIO23** | Kimenet| REL9884  |
| **Fotorezisztor**  | **GPIO19** | Bemenet| LDR      |
| **Nedv. szenzor**  | **GPIO34** | ADC    | VST581   |
| **OLED SDA**       | **GPIO21** | I2C    | SSD1306  |<img width="564" height="715" alt="Képernyőkép 2026-01-08 231820" src="https://github.com/user-attachments/assets/3cfc7457-d429-4a30-96bc-47b640ae5e02" />

| **OLED SCL**       | **GPIO22** | I2C    | SSD1306  |
| **OLED SCL**       | **GPIO22** | I2C    | SSD1306  |


**Áramkör:**
<img width="564" height="715" alt="Képernyőkép 2026-01-08 231820" src="https://github.com/user-attachments/assets/17a9553e-907e-4552-b22e-c4e19d45840f" />

## Forráskód:

### **config.py**
```python
# ---
# --- GPIO Pins ---
PUMP_RELAY_PIN: int = 23 # GPIO23
LDR_PIN: int = 19 # GPIO19
CSMS_PIN: int = 34 # GPIO34
OLED_SDA_PIN: int = 21 # GPIO21
OLED_SCL_PIN: int = 22 # GPIO22

# --- Timing Constants ---
OLED_RESET_WAIT_MS: int = 100 # 0.1 sec in ms - How much time the microcontroller should wait in the booting period for the oled to initialize.
OLED_DISPLAY_S: int = 3 # 3 sec - For how long the screen should display information.
WATERING_WAIT_S: int = 1 # 1 hour in sec - Minimum waiting time between wateing sessions of the plant !!!!!!!!!!!!!!!!
SLEEP_TIME_MS: float = 5 # 1 hour in ms - How much the microcontroller should wait between checks. !!!!!!!!!!!!
PUMP_WATERING_S: int = 1 # 5 sec - Total lenght of the watering period
PUMP_PAUSE_S: int = 5 # 5 sec - Lenght of the pauses between watering cycles in case CONTINOUS_WATERING = false

# --- Watering Settings ---
MOISTURE_AIR: int = 2451 # CSMS reference value in air.
MOISTURE_WATER: int = 863 # CSMS reference value in water.
MOISTURE_PERCENTAGE_TO_WATER_AT: float = 70.0 # At what point between the MOSITURE_AIR and MOISTURE_WATER should we start watering. Expressed in percentage.
CONTINOUS_WATERING: bool = True # True if we want to water the plant in multiple smaller water pulses. False otherwise.
WATER_ONLY_IN_DARK: bool = True # True if we only water when it's dark. False otherwise.
WATER_CYCLE_COUNT: int = 5 # If CONTINOUS_WATIRNG = True this number determines the number of watering cylces. The PUMP_WATERING_S will be divided by this number.

# --- Other Constants ---
I2C_FREQ: float = 400000 # Maximum frequency for SCL.
OLED_WIDTH: int = 128 # Width of the OLED screen.
OLED_HEIGHT: int = 32 # Height of the OLED screen.
RTC_TIMESTAMP_SIZE: int = 8 # How many bites the timestamp takes up in the RTC memory
MSG_REPEAT: int = 1 # How many times do we repeat the messages on the OLED screen.

# --- MQTT CONFIG (public) ---
MQTT_BROKER: str = "8fb34422df8e460fa89ea4ee5fbd28bf.s1.eu.hivemq.cloud"
MQTT_PORT: int = 8883
MQTT_CLIENT_ID: str = "esp32"
MQTT_TOPIC_BASE: str = "plant/device01"


# TLS settings
MQTT_USE_TLS: bool = True
'''''
```
### **main.py**
```python

# ================================
# Importok – MicroPython modulok
# ================================
import machine
from machine import Pin, ADC, I2C, RTC
import time
import ssd1306
import config
import network
from umqtt.simple import MQTTClient as mqtt
import json
import math

# -------------------------------
# Titkos adatok (WiFi, MQTT)
# -------------------------------
# A secrets.py fájl nem kerül fel GitHubra,
# ebben vannak a jelszavak és érzékeny adatok
try:
    import secrets
except ImportError:
    secrets = None

# ================================
# WiFi csatlakozás
# ================================
def connect_wifi():
    if not secrets:
        print("No WiFi secrets found")
        return False

    # WiFi újraindítása stabilabb csatlakozásért
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    time.sleep(0.1)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        
        # Maximum ~20 másodperc várakozás
        for _ in range(20):
            status = wlan.status()
            if wlan.isconnected():
                print("WiFi connected:", wlan.ifconfig())
                return True
            
            # Hibakezelés
            if status == network.STAT_WRONG_PASSWORD:
                print("Hiba: Rossz jelszó!")
                return False
            elif status == network.STAT_NO_AP_FOUND:
                print("Hiba: A WiFi hálózat nem található!")
                return False
            
            time.sleep(1)

    return wlan.isconnected()

# ================================
# MQTT csatlakozás (HiveMQ Cloud)
# ================================
def connect_mqtt():
    if not secrets:
        print("No secrets.py found, cannot connect")
        return None

    #client.username_pw_set(secrets.MQTT_USERNAME, secrets.MQTT_PASSWORD)
    client = mqtt(
        client_id=config.MQTT_CLIENT_ID,
        user=secrets.MQTT_USERNAME,
        password=secrets.MQTT_PASSWORD,
        server=config.MQTT_BROKER,
        port=config.MQTT_PORT,
        ssl=config.MQTT_USE_TLS,
        ssl_params={'server_hostname': config.MQTT_BROKER}
        )
    client.connect()
    print("Connected to HiveMQ broker")
    return client

def mqtt_publish_status(mqtt, payload: dict):
    mqtt.publish(
        f"{config.MQTT_TOPIC_BASE}/status",
        json.dumps(payload)
    )

# ================================
# Hardver inicializálás
# ================================

# Relé – vízpumpa vezérlése
relay_pin: Pin = Pin(config.PUMP_RELAY_PIN, Pin.OUT, value=0)

# Fényérzékelő (LDR)
ldr_pin: Pin = Pin(config.LDR_PIN, Pin.IN)

# Talajnedvesség szenzor (ADC)
csms_pin: ADC = ADC(config.CSMS_PIN)

# RTC – memória használata az utolsó öntözés idejének tárolására
rtc: RTC = RTC()


# ================================
# OLED kijelző inicializálása
# ================================
try:
    i2c: I2C = I2C(scl=Pin(config.OLED_SCL_PIN), sda=Pin(config.OLED_SDA_PIN), freq=config.I2C_FREQ)
    oled: SSD1306_I2C = ssd1306.SSD1306_I2C(config.OLED_WIDTH, config.OLED_HEIGHT, i2c)
    oled.poweron()
    time.sleep_ms(config.OLED_RESET_WAIT_MS)
    print("Oled screen initialized.")
except Exception as e:
    print(f'Error during the initialization of the OLED screen: {e}')
    oled = None

# ================================
# RTC memória kezelése
# ================================
def load_last_watered_time() -> int:
    value: int = 0
    try:
        data: bytes = rtc.memory()
        if data:
            value = int.from_bytes(data, 'little')
            print("'load_last_watered_time' successfully read the RTC memory.")
    except Exception:
        pass
    print(f'load_last_watered_time() -> {value}')
    return value

def save_last_watered_time(timestamp: int) -> None:
    data: bytes = timestamp.to_bytes(config.RTC_TIMESTAMP_SIZE, 'little')
    rtc.memory(data)
    print(f'last_watered_time = {timestamp}. Saved to RTC memory.')

# ================================
# Segédfüggvények
# ================================
def get_moisture_percentage(value: int) -> float:
    return ((config.MOISTURE_AIR - value) / (config.MOISTURE_AIR - config.MOISTURE_WATER)) * 100

# ================================
# Fő programlogika
# ================================
def main_loop() -> None:
    current_time: int = time.time()

    # Utolsó öntözés óta eltelt idő
    last_watered_ts: int = load_last_watered_time()
    time_elapsed_s: int = current_time - last_watered_ts

    hours: int = time_elapsed_s // 3600
    minutes: int = (time_elapsed_s % 3600) // 60

    # Szenzorok olvasása
    moisture_value: float = get_moisture_percentage(csms_pin.read())
    light_condition: str = 'Bright' if ldr_pin.value() == 1 else 'Dark'

    # Öntözési döntés
    needs_watering: bool = True
    if moisture_value > config.MOISTURE_PERCENTAGE_TO_WATER_AT:
        print(f'needs_watering = False, because moisture_value > config.MOISTURE_PERCENTAGE_TO_WATER_AT ({moisture_value} > {config.MOISTURE_PERCENTAGE_TO_WATER_AT})')
        needs_watering = False
    elif time_elapsed_s < config.WATERING_WAIT_S:
        print(f'needs_watering = False, because time_elapsed_s < config.WATERING_WAIT_S ({time_elapsed_s} < {config.WATERING_WAIT_S})')
        needs_watering = False
    elif config.WATER_ONLY_IN_DARK and light_condition == 'Bright':
        print(f"needs_watering = False, because config.WATER_ONLY_IN_DARK = True and light_condition == 'Bright' ({config.WATER_ONLY_IN_DARK} and {light_condition})")
        needs_watering = False
    
    # Öntözés végrehajtása
    if needs_watering:
        if config.CONTINOUS_WATERING:
            relay_pin.value(1)
            print('Pump relay on. Watering...')
            time.sleep(config.PUMP_WATERING_S)
            relay_pin.value(0)
        else:
            watering_time_per_cycle_s: float = config.PUMP_WATERING_S / config.WATER_CYCLE_COUNT
            for i in range(config.WATER_CYCLE_COUNT):
                relay_pin.value(1)
                print('Pump relay on. Watering...')
                time.sleep(watering_time_per_cycle_s)
                relay_pin.value(0)
                if i < config.WATER_CYCLE_COUNT - 1:
                    print('Pump relay off. Waiting...')
                time.sleep(config.PUMP_PAUSE_S)
        
        print('Pump relay off. Watering complete.')
        save_last_watered_time(current_time)
        last_watered_ts = current_time
        time_elapsed = 0
        hours = 0
        minutes = 0
    
    # OLED kijelző frissítése
    if oled:
        print('Oled display found. Displaying relevant information.')
        for i in range(config.MSG_REPEAT):
            oled.fill(0)
            oled.text('Last watered:', 0, 0)
            oled.text(f'{hours}h {minutes}m', 0, 15)
            oled.show()
            time.sleep(config.OLED_DISPLAY_S)
            
            oled.fill(0)
            oled.text(f'Check period:', 0, 0)
            oled.text(f'{config.SLEEP_TIME_MS // 60000} minutes', 0, 15)
            oled.show()
            time.sleep(config.OLED_DISPLAY_S)
            
            oled.fill(0)
            status_msg = f'Light: {light_condition}'
            if needs_watering:
                status_msg = 'Just watered!'
            
            oled.text(f'{status_msg}', 0, 0)
            oled.text(f'Moisture: {moisture_value}', 0, 15)

            oled.show()
            time.sleep(config.OLED_DISPLAY_S)
        
        oled.fill(0)
        oled.text('Z Z Z', 80, 0)
        oled.text(' ( - - )', 0, 16)
        oled.text('   ---  ', 0, 24)
        oled.text('RST TO', 80, 16)
        oled.text('WAKE', 80, 24)
        oled.show()
    
    # MQTT adatküldés
    client = connect_mqtt()
    if not client:
            return

    for i in range(5):
        payload = {
            "moisture": math.ceil(moisture_value),
            "light": light_condition,
            "needs_watering": needs_watering,
            "timestamp": current_time
        }
        mqtt_publish_status(client, payload)
        time.sleep(5)

    client.disconnect()
    print("Payload sent")

    print(f'Going to sleep for {config.SLEEP_TIME_MS // 1000} seconds...')

    #machine.deepsleep(config.SLEEP_TIME_MS)

# ================================
# Program belépési pont
# ================================
if __name__ == '__main__':
    if connect_wifi():
        main_loop()
    else:
        print("Nem sikerült a WiFi csatlakozás, a program leáll.")
```

### **mqqt_test.py**
```python
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
```

### **ssd1306.py**
```python
# MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from micropython import const
import framebuf


# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,  # off
            # address setting
            SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            SET_CONTRAST,
            0xFF,  # maximum
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            # charge pump
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,
        ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)


class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time

        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)
```

## Képek a készítésről és végeredményről 

**HiveMQ Dashboard beállítás:**
![HiveMQ Dashboard](https://github.com/user-attachments/assets/664400ff-c0f9-43c4-ac2d-f5dd64fba984)

**Node-RED Flow & Dashboard:**
![Bekötés 1](https://github.com/user-attachments/assets/97796e44-7a63-43b0-a69d-d22d60c88ec9)
![Bekötés 2](https://github.com/user-attachments/assets/a750ac9a-7d63-4484-aeec-c7ea7be5327a)
![Bekötés 3](https://github.com/user-attachments/assets/e77c480f-c3ca-4637-a125-018d6aba5121)

**Prototípus:**
![Node-RED Flow](https://github.com/user-attachments/assets/57bde317-ff7c-47dc-bdd7-3d902576d621)
![Web Dashboard](https://github.com/user-attachments/assets/ba89acc6-48fb-48b9-8388-c642a7453b7e)

**Rövid bemutató a működésről:**
[![Demo](./docs/Demo.MOV)](./docs/Demo.MOV)



