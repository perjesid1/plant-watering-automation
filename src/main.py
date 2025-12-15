import machine
from machine import Pin, ADC, I2C, RTC
import time
import ssd1306
import config
import network
from umqtt.simple import MQTTClient
import json

try:
    import secrets
except ImportError:
    secrets = None

def connect_wifi():
    if not secrets:
        print("No WiFi secrets found")
        return False

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        for _ in range(20):
            if wlan.isconnected():
                print("WiFi connected:", wlan.ifconfig())
                return True
            time.sleep(1)

    return wlan.isconnected()

def connect_mqtt():
    client = MQTTClient(
        client_id=config.MQTT_CLIENT_ID,
        server=config.MQTT_BROKER,
        port=config.MQTT_PORT,
        keepalive=60
    )
    client.connect()
    print("Connected to MQTT broker")
    return client

def mqtt_publish_status(mqtt, payload: dict):
    mqtt.publish(
        f"{config.MQTT_TOPIC_BASE}/status",
        json.dumps(payload)
    )

relay_pin: Pin = Pin(config.PUMP_RELAY_PIN, Pin.OUT, value=0)
ldr_pin: Pin = Pin(config.LDR_PIN, Pin.IN)
csms_pin: ADC = ADC(config.CSMS_PIN)

rtc: RTC = RTC()

try:
    i2c: I2C = I2C(scl=Pin(config.OLED_SCL_PIN), sda=Pin(config.OLED_SDA_PIN), freq=config.I2C_FREQ)
    oled: SSD1306_I2C = ssd1306.SSD1306_I2C(config.OLED_WIDTH, config.OLED_HEIGHT, i2c)
    oled.poweron()
    time.sleep_ms(config.OLED_RESET_WAIT_MS)
    print("Oled screen initialized.")
except Exception as e:
    print(f'Error during the initialization of the OLED screen: {e}')
    oled = None

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

def get_moisture_percentage(value: int) -> float:
    return ((config.MOISTURE_AIR - value) / (config.MOISTURE_AIR - config.MOISTURE_WATER)) * 100

def main_loop() -> None:
    current_time: int = time.time()

    last_watered_ts: int = load_last_watered_time()
    time_elapsed_s: int = current_time - last_watered_ts

    hours: int = time_elapsed_s // 3600
    minutes: int = (time_elapsed_s % 3600) // 60

    moisture_value: float = get_moisture_percentage(csms_pin.read())
    light_condition: str = 'Bright' if ldr_pin.value() == 1 else 'Dark'

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
    
    print(f'Going to sleep for {config.SLEEP_TIME_MS // 1000} seconds...')

    machine.deepsleep(config.SLEEP_TIME_MS)

if __name__ == '__main__':
    main_loop()
