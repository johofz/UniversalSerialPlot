from PyQt5.QtCore import QThread, pyqtSignal
import serial
import numpy as np


class SerialReadThread(QThread):
    data_received = pyqtSignal(bytes)  # Signal für empfangene Daten

    def __init__(self, serial_connection, dtype_func, parent=None):
        super().__init__(parent)
        self.serial_connection = serial_connection
        self._is_running = True
        self.get_dtype = dtype_func  # Funktion, die den aktuellen dtype zurückgibt

    def run(self):
        while self._is_running:
            try:
                # Hole den aktuellen dtype
                dtype = self.get_dtype()
                bytes_to_read = dtype.itemsize  # Anzahl der zu lesenden Bytes basierend auf dtype

                # Echte Daten von der seriellen Verbindung lesen
                data = self.serial_connection.read(bytes_to_read)

                if len(data) == bytes_to_read:
                    # Signal senden, wenn alle Bytes empfangen wurden
                    self.data_received.emit(data)

            except serial.SerialException as e:
                print(f"Fehler beim Lesen der seriellen Daten: {e}")
                self._is_running = False  # Stoppe den Thread bei einem Fehler

    def stop(self):
        self._is_running = False
        if self.serial_connection.is_open:
            self.serial_connection.close()
        self.quit()
