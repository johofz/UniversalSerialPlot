from PyQt5.QtCore import QThread, pyqtSignal
from bleak import BleakClient
import asyncio


class BLEThread(QThread):
    data_received = pyqtSignal(bytes)  # Signal für empfangene Daten

    def __init__(self, ble_address, ble_uuid, parent=None):
        super().__init__(parent)
        self.ble_address = ble_address
        self.ble_uuid = ble_uuid
        self._is_running = True

    async def connect_and_subscribe(self):
        async with BleakClient(self.ble_address) as client:
            # print(f"Verbunden mit {self.ble_address}")

            def notification_handler(sender, data):
                # print(f"Benachrichtigung von {sender}: {data}")

                # Konvertiere bytearray in bytes
                if isinstance(data, bytearray):
                    data = bytes(data)

                # Sende die konvertierten Daten weiter
                self.data_received.emit(data)

            await client.start_notify(self.ble_uuid, notification_handler)

            while self._is_running:
                await asyncio.sleep(1)  # BLE-Verbindung aktiv halten

            await client.stop_notify(self.ble_uuid)

    def run(self):
        asyncio.run(self.connect_and_subscribe())

    def stop(self):
        self._is_running = False
        self.quit()
