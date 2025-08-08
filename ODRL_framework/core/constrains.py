# ordl_framework/core/constraints.py

def validate_frequency_range(freq_range):
    freq_min, freq_max = freq_range
    if freq_min >= freq_max:
        raise ValueError("Invalid frequency range: min >= max")
