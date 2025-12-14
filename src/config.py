# --- GPIO Pins ---
PUMP_RELAY_PIN: int = 23 # GPIO23
LDR_PIN: int = 19 # GPIO19
CSMS_PIN: int = 34 # GPIO34
OLED_SDA_PIN: int = 21 # GPIO21
OLED_SCL_PIN: int = 22 # GPIO22

# --- Timing Constants ---
OLED_RESET_WAIT_MS: int = 100 # 0.1 sec in ms - How much time the microcontroller should wait in the booting period for the oled to initialize.
OLED_DISPLAY_S: int = 3 # 3 sec - For how long the screen should display information.
WATERING_WAIT_S: int = 3600 # 1 hour in sec - Minimum waiting time between wateing sessions of the plant
SLEEP_TIME_MS: float = 3600000 # 1 hour in ms - How much the microcontroller should wait between checks.
PUMP_WATERING_S: int = 5 # 5 sec - Total lenght of the watering period
PUMP_PAUSE_S: int = 5 # 5 sec - Lenght of the pauses between watering cycles in case CONTINOUS_WATERING = false

# --- Watering Settings ---
MOISTURE_AIR: int = 2451 # CSMS reference value in air.
MOISTURE_WATER: int = 863 # CSMS reference value in water.
MOISTURE_PERCENTAGE_TO_WATER_AT: float = 50.0 # At what point between the MOSITURE_AIR and MOISTURE_WATER should we start watering. Expressed in percentage.
CONTINOUS_WATERING: bool = True # True if we want to water the plant in multiple smaller water pulses. False otherwise.
WATER_ONLY_IN_DARK: bool = True # True if we only water when it's dark. False otherwise.
WATER_CYCLE_COUNT: int = 5 # If CONTINOUS_WATIRNG = True this number determines the number of watering cylces. The PUMP_WATERING_S will be divided by this number.

# --- Other Constants ---
I2C_FREQ: float = 400000 # Maximum frequency for SCL.
OLED_WIDTH: int = 128 # Width of the OLED screen.
OLED_HEIGHT: int = 32 # Height of the OLED screen.
RTC_TIMESTAMP_SIZE: int = 8 # How many bites the timestamp takes up in the RTC memory
MSG_REPEAT: int = 3 # How many times do we repeat the messages on the OLED screen.

# --- MQTT ---
