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

## Használt források 🛠️

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
| **OLED SDA**       | **GPIO21** | I2C    | SSD1306  |
| **OLED SCL**       | **GPIO22** | I2C    | SSD1306  |


Forráskód, megjegyzésekkel!



## Képek a készítésről és végeredményről 📸

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
- 1. Indulás (ESP32 felébred):
WiFi connect → MQTT HiveMQ → szenzorok init

- 2. Mérés (5 mp):

Talajnedvesség: 65% (GPIO34) → SZÁRAZ ❌
Fény: Dark (GPIO19)
Eltelt: 1h 15p (RTC memória)

- 3. Öntözés (ha kell):
Relé ON (GPIO23) → pumpa 1 mp → OFF
Új timestamp RTC-be

-4. Kijelzés & kommunikáció:
OLED: "Just watered!" + 65%
MQTT: {"moisture":65,"needs_watering":true}
Node-RED dashboard frissül

-5. Alvás:
deepsleep(5 mp) → következő mérés
Ciklus ismétlődik! 🌱💧

