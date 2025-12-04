from machine import Pin
from exceptions import HardwareInitError
from exceptions import SensorError

class LDR:
    """Photoresistor class."""
    def __init__(self, name:str,  pin:Pin) -> None:
        """
        Initialises the photoresistor.

        Args:
            name (str): Name of the device.
            pin (Pin): The GPIO Pin used by the device.
        
        Returns:
            None
        
        Raises:
            HardwareInitError
        """
        try:
            self.name = name
            self.ldr_pin = machine.ADC(pin)
            print(f"Photoresistor '{self.name}' successfully initialized.")
        except Exception as e:
            raise HardwareInitError(f"Unable to initialize Photoresistor '{self.name}': {str(e)}") from e
    
        
    def get_raw_value(self) -> int:
        """
        Reads the raw value provided by the Photoresistor.

        Args:
            None
        
        Returns:
            (int) The current value provided by the photoresistor
        
        Raises:
            SensorError
        """
        try:
            value: int = self.ldr_pin.read_u16()
            print(f"Photoresistor '{self.name}' raw value read: {value}")
            return value
        except Exception as e:
            raise SensorError(f"Photoresistor '{self.name}' is unable to read data: {str(e)}") from e
    
    def get_light_percentage(self) -> float:
        """
        Reads the value provided by the Photoresistor.

        Args:
            None
        
        Returns:
            (float) The current value provided by the photoresistor in percentages.
        
        Raises:
            SensorError
        """
        try:
            value: float = round(self.get_raw_value()/65535*100,2)
            print(f"Photoresistor '{self.name}' percentage value read: {value}%")
            return value
        except Exception as e:
            raise SensorError(f"Photoresistor '{self.name}' is unable to read data: {str(e)}") from e