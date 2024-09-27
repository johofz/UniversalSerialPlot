import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTabWidget, QWidget, QSlider
from PyQt5.QtCore import Qt
from serial_configurator import SerialConfigurator
from dtype_configurator import DtypeConfigurator
from mpl_canvas import MplCanvas

# Hauptfenster der Anwendung


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hauptlayout und Tabs
        self.tabs = QTabWidget()
        self.main_layout = QVBoxLayout()

        # Tab für den Live-Plot
        self.data_tab = QWidget()
        self.init_data_tab()

        # Tab für den Dtype-Konfigurator
        self.config_tab = QWidget()
        self.dtype_configurator = DtypeConfigurator()
        self.init_config_tab()

        # Tab für die serielle Konfiguration
        self.serial_config_tab = QWidget()
        self.serial_configurator = SerialConfigurator(self)
        self.init_serial_config_tab()

        # Tabs zum Hauptlayout hinzufügen
        self.tabs.addTab(self.data_tab, "Live-Plot")
        self.tabs.addTab(self.config_tab, "Dtype Konfigurator")
        self.tabs.addTab(self.serial_config_tab, "Serielle Konfiguration")

        # Zentrales Widget setzen
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.tabs)
        self.setCentralWidget(self.central_widget)

        # Fensterkonfiguration
        self.setWindowTitle('Live-Plot und Konfiguration')
        self.setGeometry(100, 100, 800, 600)

    def init_data_tab(self):
        layout = QVBoxLayout()

        # Matplotlib-Canvas (Live-Plot)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

        # Schieberegler hinzufügen
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(100)  # Minimum 100 Werte anzeigen
        self.slider.setMaximum(10000)  # Maximum 10.000 Werte
        self.slider.setValue(1000)  # Standardwert auf 1000
        self.slider.setTickInterval(100)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.update_view_size)
        layout.addWidget(self.slider)

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
        # Aktualisiere die Anzahl der anzuzeigenden Datenpunkte basierend auf dem Schieberegler
        view_size = self.slider.value()
        self.canvas.set_view_size(view_size)


# Hauptprogramm
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
