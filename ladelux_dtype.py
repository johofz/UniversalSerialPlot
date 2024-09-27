import numpy as np

Ladelux_dtype = np.dtype([
    # Schalter Felder
    ('temperatureMCU_degC', 'int16'),
    ('usbCurrent_mA', 'int16'),
    ('usbVoltage_mV', 'uint16'),
    ('userRequest', 'uint8'),
    ('error_tx', 'uint8'),  # Umbenannt, um Verwechslungen zu vermeiden
    ('crc_tx', 'uint16'),

    # Scheinwerfer Felder
    ('SOC', 'uint8'),
    ('battery_voltage_mV', 'uint16'),
    ('battery_current_mA', 'int16'),
    ('system_power_mW', 'uint16'),
    ('dynamo_frequency_Hz', 'uint16'),
    ('batteryState', 'uint8'),
    ('lightState', 'uint8'),
    ('error_rx', 'uint8'),  # Umbenannt, um Verwechslungen zu vermeiden
    ('crc_rx', 'uint16'),
])
