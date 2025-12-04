import machine
from machine import Pin, ADC, I2C, RTC
import time
import ssd1306
import config

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
    try:
        data = rtc.memory()
        if data:
            return int.from_bytes(data, 'little')
    except Exception:
        pass
    return 0

def save_last_watered_time(timestamp) -> None:
    data = timestamp.to_bytes(config.RTC_ADDR_LAST_WATERED_END, 'little')
    rtc.memory(data)

def main_loop():
    current_time = time.time()

    last_watered_ts = load_last_watered_time()
    time_elapsed_s = current_time - last_watered_ts

    hours = time_elapsed_s // 3600
    minutes = (time_elapsed_s % 3600) // 60

    moisture_value = csms_pin.read()
    light_condition = 'Bright' if ldr_pin.value() == 1 else 'Dark'

    needs_watering = False
    if moisture_value < config.MOISTURE_THRESHOLD and time_elapsed_s > config.WATERING_WAIT_S:
        relay_pin.value(1)
        time.sleep(config.PUMP_WATERING_S)
        relay_pin.value(0)
        save_last_watered_time(current_time)
        last_watered_ts = current_time
        time_elapsed_s = 0
        hours = 0
        minutes = 0
        needs_watering = True
    
    if oled:
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
    print(f'Last Watered TS: {last_watered_ts}')

    machine.deepsleep(config.SLEEP_TIME_MS)

if __name__ == '__main__':
    main_loop()