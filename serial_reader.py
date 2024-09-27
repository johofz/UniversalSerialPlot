from PyQt5.QtCore import QThread, pyqtSignal
import serial

# Thread zum asynchronen Lesen der seriellen Daten


class SerialReadThread(QThread):
    # Signal, das Daten sendet, wenn sie gelesen werden
    data_received = pyqtSignal(bytes)

    def __init__(self, serial_connection, dtype_func, parent=None):
        super().__init__(parent)
        self.serial_connection = serial_connection
        self._is_running = True
        self.get_dtype = dtype_func  # Funktion, die den aktuellen dtype zurückgibt

    def run(self):
        while self._is_running:
            current_dtype = self.get_dtype()  # Den aktuellen dtype abrufen
            read_size = current_dtype.itemsize  # Bestimme die Anzahl der zu lesenden Bytes
            if self.serial_connection.in_waiting >= read_size:
                # Lese die entsprechende Anzahl an Bytes
                data = self.serial_connection.read(read_size)
                # Sende die gelesenen Daten an die Hauptanwendung
                self.data_received.emit(data)

    def stop(self):
        self._is_running = False
        self.serial_connection.close()
        self.quit()
