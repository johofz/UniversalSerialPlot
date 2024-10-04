from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import pyqtSignal, QThread
from bleak import BleakScanner
import asyncio


class BLEConfigurator(QWidget):
    # Signal für ausgewähltes Gerät und UUID
    ble_device_selected = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        # Geräteauswahl
        self.device_selector = QComboBox(self)
        self.layout.addWidget(QLabel("BLE-Gerät:"))
        self.layout.addWidget(self.device_selector)

        # Scan-Button
        self.scan_button = QPushButton("Geräte scannen", self)
        self.scan_button.clicked.connect(self.start_ble_scan_thread)
        self.layout.addWidget(self.scan_button)

        # Connect-Button
        self.connect_button = QPushButton("Verbinden", self)
        self.connect_button.clicked.connect(self.connect_to_ble_device)
        self.layout.addWidget(self.connect_button)

        self.setLayout(self.layout)

    def start_ble_scan_thread(self):
        self.scan_thread = BLEScanThread(self)
        self.scan_thread.devices_found.connect(self.update_device_selector)
        self.scan_thread.start()

    def update_device_selector(self, devices):
        """Aktualisiere die Geräteliste in der ComboBox."""
        self.device_selector.clear()
        for name, address in devices:
            self.device_selector.addItem(f"{name} ({address})", address)

    def connect_to_ble_device(self):
        selected_device = self.device_selector.currentData()
        # Verwende hier eine passende UUID für die GATT-Characteristic
        self.ble_device_selected.emit(
            selected_device, "b088b5a2-08fe-4655-af55-1c69c8917659")


class BLEScanThread(QThread):
    devices_found = pyqtSignal(list)  # Signal, um gefundene Geräte zu senden

    def run(self):
        devices = asyncio.run(self.scan_for_devices())
        self.devices_found.emit(devices)

    async def scan_for_devices(self):
        devices = await BleakScanner.discover()
        device_list = [(device.name, device.address) for device in devices]
        return device_list
