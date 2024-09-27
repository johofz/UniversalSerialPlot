import serial.tools.list_ports
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from serial_reader import SerialReadThread
import numpy as np


class SerialConfigurator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.serial_connection = None  # Placeholder für die serielle Verbindung
        self.serial_thread = None  # Placeholder für den SerialReadThread
        self.parent_window = parent

        self.layout = QVBoxLayout()

        # Auswahl für den seriellen Port
        self.port_selector = QComboBox(self)
        self.update_serial_ports()  # Dynamisch die Ports abrufen
        self.layout.addWidget(QLabel("Serieller Port:"))
        self.layout.addWidget(self.port_selector)

        # Button zum Refresh der Ports
        self.refresh_button = QPushButton("Ports aktualisieren", self)
        self.refresh_button.clicked.connect(self.update_serial_ports)
        self.layout.addWidget(self.refresh_button)

        # Auswahl für die Baudrate
        self.baudrate_selector = QComboBox(self)
        self.baudrate_selector.addItems(
            ["9600", "19200", "38400", "57600", "115200"])
        self.layout.addWidget(QLabel("Baudrate:"))
        self.layout.addWidget(self.baudrate_selector)

        # Button zum Verbinden
        self.connect_button = QPushButton("Verbinden", self)
        self.connect_button.clicked.connect(self.connect_to_serial_port)
        self.layout.addWidget(self.connect_button)

        self.setLayout(self.layout)

    def update_serial_ports(self):
        # Verfügbare serielle Ports abrufen und ComboBox aktualisieren
        ports = serial.tools.list_ports.comports()
        self.port_selector.clear()  # Vorherige Einträge löschen
        for port in ports:
            self.port_selector.addItem(port.device)

    def connect_to_serial_port(self):
        # Verbindung mit dem ausgewählten seriellen Port herstellen
        port = self.port_selector.currentText()
        baudrate = self.baudrate_selector.currentText()

        try:
            self.serial_connection = serial.Serial(port, baudrate, timeout=1)
            print(f"Verbunden mit {port} bei {baudrate} Baud.")

            # Starte den Thread zum Lesen der Daten
            self.serial_thread = SerialReadThread(
                self.serial_connection, self.parent_window.dtype_configurator.get_dtype)
            self.serial_thread.data_received.connect(self.handle_serial_data)
            self.serial_thread.start()

        except serial.SerialException as e:
            print(f"Fehler bei der Verbindung: {e}")

    def handle_serial_data(self, data):
        # Verarbeite die empfangenen seriellen Daten
        print(f"Empfangene serielle Daten: {data}")

        try:
            dtype = self.parent_window.dtype_configurator.get_dtype()
            expected_size = dtype.itemsize

            if len(data) != expected_size:
                raise ValueError(
                    f"Ungültige Datenlänge: Erwartet {expected_size} Bytes, aber {len(data)} Bytes erhalten.")

            # Dekodiere die Daten
            decoded_data = np.frombuffer(data, dtype=dtype)
            print(f"Decodierte Daten: {decoded_data}")

            # Ermitteln, welche Felder geplottet werden sollen
            plot_fields = self.parent_window.dtype_configurator.get_plot_fields()
            print(f"Felder zum Plotten: {plot_fields}")

            # Plot initialisieren, wenn sich die ausgewählten Felder ändern
            self.parent_window.canvas.init_plot(plot_fields)

            # Neue Daten für die zu plottenden Felder sammeln
            plot_data = {field: decoded_data[field] for field in plot_fields}

            # Aktualisiere den Plot mit den neuen Daten
            self.parent_window.canvas.update_plot(plot_data)

        except ValueError as ve:
            print(f"Fehler beim Verarbeiten der seriellen Daten: {ve}")
        except TypeError as te:
            print(f"Fehler beim Dekodieren der Daten mit np.frombuffer: {te}")
        except Exception as e:
            print(f"Allgemeiner Fehler: {e}")

    def close_serial_connection(self):
        if self.serial_thread is not None:
            self.serial_thread.stop()
            self.serial_thread = None
        print("Serielle Verbindung geschlossen.")
