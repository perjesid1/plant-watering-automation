"""This module contains the custom exceptions used by the application."""

class HardwareInitError(Exception):
    """
    Error during the initialization of a hardware component.
    """
    pass

class SensorError(Exception):
    """
    A sensor experiences a problem.
    """
    pass

class ActuatorError(Exception):
    """
    An actuator experiences a problem.
    """
    pass