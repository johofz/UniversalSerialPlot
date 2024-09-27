from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np
import time


class SerialReadThread(QThread):
    data_received = pyqtSignal(bytes)  # Signal für empfangene Daten

    def __init__(self, serial_connection, dtype_func, parent=None):
        super().__init__(parent)
        self.serial_connection = serial_connection
        self._is_running = True
        self.get_dtype = dtype_func  # Funktion, die den aktuellen dtype zurückgibt

    def run(self):
        while self._is_running:
            # Simuliere das Erzeugen von Dummy-Daten, falls keine seriellen Daten empfangen werden
            dummy_data = self.generate_dummy_data()
            print(f"Erzeugte Dummy-Daten: {dummy_data}")
            # Dummy-Daten als Signal senden
            self.data_received.emit(dummy_data)
            time.sleep(0.1)  # Simuliere eine kleine Wartezeit

    def stop(self):
        self._is_running = False
        if self.serial_connection.is_open:
            self.serial_connection.close()
        self.quit()

    def generate_dummy_data(self):
        # Erzeuge Dummy-Daten entsprechend dem aktuellen dtype
        dtype = self.get_dtype()
        dummy_values = np.zeros(1, dtype=dtype)

        # Beispieldaten zufällig generieren
        for field in dtype.fields:
            if np.issubdtype(dtype[field], np.integer):
                dummy_values[field] = np.random.randint(0, 255)
            else:
                dummy_values[field] = np.random.uniform(0, 100)

        return dummy_values.tobytes()
