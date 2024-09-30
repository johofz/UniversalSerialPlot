import serial.tools.list_ports
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from serial_reader import SerialReadThread
import serial
import numpy as np
from ring_buffer import RingBuffer


class SerialConfigurator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.serial_connection = None  # Placeholder für die serielle Verbindung
        self.serial_thread = None  # Placeholder für den SerialReadThread
        self.parent_window = parent

        self.layout = QVBoxLayout()

        # Ring-Buffer mit einer Kapazität von 10.000 Werten initialisieren
        self.ring_buffer = RingBuffer(
            size=10000, dtype=self.parent_window.dtype_configurator.get_dtype())

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

        # Button zum Trennen der Verbindung
        self.disconnect_button = QPushButton("Verbindung trennen", self)
        self.disconnect_button.clicked.connect(self.close_serial_connection)
        self.layout.addWidget(self.disconnect_button)

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
        # Speichern der Daten im Ring-Buffer
        dtype = self.parent_window.dtype_configurator.get_dtype()
        decoded_data = np.frombuffer(data, dtype=dtype)
        # print(f"Empfangene serielle Daten: {decoded_data}")

        # Jedes empfangene Datenpaket in den Ring-Buffer speichern
        self.ring_buffer.append(decoded_data)

        # Optional: Die gesamten Daten aus dem Ring-Buffer abrufen
        buffer_data = self.ring_buffer.get()

        # Ermitteln, welche Felder geplottet werden sollen
        plot_fields = self.parent_window.dtype_configurator.get_plot_fields()
        # print(f"Felder zum Plotten: {plot_fields}")

        # Plot initialisieren, wenn sich die ausgewählten Felder ändern
        self.parent_window.canvas.init_plot(plot_fields)

        # Die tatsächliche Anzahl der Daten im Ring-Buffer bestimmen
        current_size = len(buffer_data)

        # Neue Daten für die zu plottenden Felder sammeln
        plot_data = {field: buffer_data[field].flatten()
                    for field in plot_fields}

        # Aktualisiere den Plot mit den neuen Daten
        self.parent_window.canvas.update_plot(plot_data, current_size)


    def close_serial_connection(self):
        # Schließe die serielle Verbindung und stoppe den Thread
        if self.serial_thread is not None:
            self.serial_thread.stop()
            self.serial_thread = None

        if self.serial_connection is not None and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None

        print("Serielle Verbindung geschlossen.")
