# --- GPIO Pins ---
PUMP_RELAY_PIN: int = 4 #D2
LDR_PIN: int = 5 #D1
CSMS_PIN: int = 0 #A0
OLED_SDA_PIN: int = 0 #D3
OLED_SCL_PIN: int = 2 #D4

# --- Timing Constants ---
OLED_RESET_WAIT_MS: int = 100 # 0.1 sec in ms
OLED_DISPLAY_S: int = 5 # 5 sec
WATERING_WAIT_S: int = 3600 # 1 hour
SLEEP_TIME_MS: float = 3600000 # 1 hour in ms
PUMP_WATERING_S: int = 5 # 5 sec


# --- Other Constants ---
I2C_FREQ: float = 400000
OLED_WIDTH: int = 128
OLED_HEIGHT: int = 32
MOISTURE_THRESHOLD: int = 500
RTC_ADDR_LAST_WATERED_START: int = 0
RTC_ADDR_LAST_WATERED_END: int = 8
MSG_REPEAT: int = 3