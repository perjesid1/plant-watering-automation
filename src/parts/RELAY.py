from machine import Pin
from enum import Enum
from exceptions import HardwareInitError
from exceptions import ActuatorError

class RelayType(Enum):
    """
    Relay Type enum.
    NC - Normally Closed
    NO - Normally Open
    """
    NO = 0
    NC = 1

class RelayDevice:
    """
    Relay Device class.
    """
    def __init__(self, name:str, pin:Pin, type:RelayType) -> None:
        """
        Initialises the relay device.

        Args:
            name (str): Name of the device.
            pin (Pin): The GPIO Pin used by the device.
            type (RelayType): The type of the relay device (Normally Open or Normally Closed).

        Returns:
            None

        Raises:
            HardwareInitError
        """
        try:
            self.pin: Pin = pin
            self.name: str = name
            self.type: RelayType = type
            self.off()
            
            print(f"Relay Device '{self.name}' successfully initialized.")
        except Exception as e:
            raise HardwareInitError(f"Unable to initialize {self.name} relay device: {str(e)}") from e
    
    def on(self) -> None:
        """
        Turns on the relay device.
        "On" means that the relay gives electricity on it's output.
        For NO Relays, it means a LOW signal.
        For NC Relays, it means a HIGH signal.

        Args:
            None

        Returns:
            None

        Raises:
            ActuatorError
        """
        print(f"Turning on '{self.name}' relay device...")
        if self.type == RelayType.NC:
            self.pin.value(1)
        elif self.type == RelayType.NO:
            self.pin.value(0)
        else:
            raise ActuatorError(f"Unknown relay type for '{self.name}' relay: {self.type}")
    
    def off(self) -> None:
        """
        Turns off the relay device.
        "Off" means that the relay does not give electricity on it's output.
        For NO Relays, it means a HIGH signal.
        For NC Relays, it means a LOW signal.

        Args:
            None

        Returns:
            None

        Raises:
            ActuatorError
        """
        print(f"Turning off '{self.name}' relay device...")
        if self.type == RelayType.NC:
            self.pin.value(0)
        elif self.type == RelayType.NO:
            self.pin.value(1)
        else:
            raise ActuatorError(f"Unknown relay type for '{self.name}' relay: {self.type}")
