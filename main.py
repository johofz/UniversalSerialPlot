# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from serial_configurator import SerialConfigurator
from dtype_configurator import DtypeConfigurator
from mpl_canvas import MplCanvas
# Importiere das Stylesheet aus dark_theme.py
from dark_theme import get_dark_theme
from ble_configurator import BLEConfigurator
from ble_thread import BLEThread
import numpy as np
from ring_buffer import RingBuffer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Wende das Dark-Theme-Stylesheet an
        self.setStyleSheet(get_dark_theme())

        # Layout und Tabs
        self.setup_ui()

    def setup_ui(self):
        self.tabs = QTabWidget()
        self.main_layout = QVBoxLayout()

        self.data_tab = QWidget()
        self.init_data_tab()

        self.config_tab = QWidget()
        self.dtype_configurator = DtypeConfigurator()
        self.init_config_tab()

        self.serial_config_tab = QWidget()
        self.serial_configurator = SerialConfigurator(self)
        self.init_serial_config_tab()

        self.ble_tab = QWidget()
        self.ble_configurator = BLEConfigurator()
        self.ble_configurator.ble_device_selected.connect(
            self.start_ble_thread)
        self.init_ble_tab()

        self.tabs.addTab(self.data_tab, "Live-Plot")
        self.tabs.addTab(self.config_tab, "Dtype Konfigurator")
        self.tabs.addTab(self.serial_config_tab, "Serielle Konfiguration")
        self.tabs.addTab(self.ble_tab, "BLE Konfiguration")

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.tabs)
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle('Live-Plot und Konfiguration')
        self.setGeometry(100, 100, 800, 600)

        # Initialisiere den Ring-Buffer
        self.ring_buffer = RingBuffer(
            size=1000, dtype=self.dtype_configurator.get_dtype())

    def init_data_tab(self):
        layout = QVBoxLayout()

        # Matplotlib-Canvas (Live-Plot)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

        # Horizontal Layout für Slider und Label
        slider_layout = QHBoxLayout()

        # Slider hinzufügen
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(1000)
        self.slider.setValue(100)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.update_view_size)
        slider_layout.addWidget(self.slider)

        # Label zum Anzeigen des Slider-Werts (begrenzte Höhe)
        self.slider_label = QLabel(
            f"Datenpunkte: {self.slider.value()}", self)
        self.slider_label.setStyleSheet("font-size: 15px;")  # Kleinere Schrift
        self.slider_label.setFixedHeight(20)  # Höhe auf 20px festlegen
        slider_layout.addWidget(self.slider_label)

        # Füge das horizontal Layout dem Hauptlayout hinzu
        layout.addLayout(slider_layout)

        self.data_tab.setLayout(layout)

    def init_config_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(self.dtype_configurator)
        self.config_tab.setLayout(layout)

    def init_serial_config_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(self.serial_configurator)
        self.serial_config_tab.setLayout(layout)

    def update_view_size(self):
        view_size = self.slider.value()
        self.canvas.set_view_size(view_size)
        self.slider_label.setText(f"Datenpunkte: {view_size}")

    def init_ble_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(self.ble_configurator)
        self.ble_tab.setLayout(layout)

    def start_ble_thread(self, address, uuid):
        # Startet den BLE-Thread für die Verbindung
        self.ble_thread = BLEThread(address, uuid)
        self.ble_thread.data_received.connect(self.handle_ble_data)
        self.ble_thread.start()

    def handle_ble_data(self, data):
        # Hier landen die Daten, die über BLE empfangen wurden
        # print(f"Empfangene BLE-Daten: {data}")

        # Verarbeite die empfangenen BLE-Daten (z.B. CRC-Validierung, Plotten)
        dtype = self.dtype_configurator.get_dtype()
        decoded_data = np.frombuffer(data, dtype=dtype)
        print(decoded_data)

        # Die dekodierten Daten können jetzt in den Plot integriert werden
        self.ring_buffer.append(decoded_data)
        self.update_plot()

    def update_plot(self):
        """Aktualisiert den Plot mit den Daten aus dem Ring-Buffer."""
        # Hole die Daten aus dem Ring-Buffer
        buffer_data = self.ring_buffer.get()

        # Ermitteln, welche Felder geplottet werden sollen
        plot_fields = self.dtype_configurator.get_plot_fields()
        print(f"Felder zum Plotten: {plot_fields}")
        print(f"Verfügbare Datenfelder: {buffer_data.dtype.names}")

        # Plot initialisieren, wenn sich die ausgewählten Felder ändern
        self.canvas.init_plot(plot_fields)

        # Neue Daten für die zu plottenden Felder sammeln
        plot_data = {}
        for field in plot_fields:
            if field in buffer_data.dtype.names:
                plot_data[field] = buffer_data[field].flatten()
            else:
                print(
                    f"Warnung: Feld '{field}' nicht in den empfangenen Daten gefunden.")

        # Bestimme die aktuelle Größe der Daten im Buffer
        current_size = len(buffer_data)

        # Aktualisiere den Plot mit den neuen Daten
        self.canvas.update_plot(plot_data, current_size)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
