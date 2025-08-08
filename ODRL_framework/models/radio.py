# ordl_framework/models/radio.py
from ODRL_framework.core.constrains import validate_frequency_range

class Radio:
    def __init__(self, name, frequency_range, bandwidth, modulations, interfaces):
        validate_frequency_range(frequency_range)
        self.name = name
        self.frequency_range = frequency_range
        self.bandwidth = bandwidth
        self.modulations = modulations
        self.interfaces = interfaces
