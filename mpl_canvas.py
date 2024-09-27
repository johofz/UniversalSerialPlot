from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.lines = {}  # Dictionary für Linien
        self.buffer_size = 10000  # Speichertiefe auf 10.000 setzen
        self.data_buffer = {}  # Speicher für die Daten
        self.current_view_size = 1000  # Anzahl der Datenpunkte, die angezeigt werden

    def init_plot(self, fields):
        # Initialisiere den Plot für die ausgewählten Felder
        self.axes.clear()
        self.lines = {}
        # Initialisiere Datenpuffer
        self.data_buffer = {field: np.zeros(
            self.buffer_size) for field in fields}

        # x-Achse mit der Speichertiefe
        self.t = np.linspace(0, self.buffer_size - 1, self.buffer_size)
        for field in fields:
            line, = self.axes.plot(self.t[:self.current_view_size], np.zeros(
                self.current_view_size), label=field)
            self.lines[field] = line

        self.axes.legend()
        self.draw()

    def update_plot(self, data):
        # Aktualisiere den Puffer mit neuen Daten
        for field, new_data in data.items():
            self.data_buffer[field] = np.roll(
                self.data_buffer[field], -len(new_data))  # Älteste Daten entfernen
            # Neue Daten am Ende hinzufügen
            self.data_buffer[field][-len(new_data):] = new_data

        # Zeige nur die aktuelle View an, basierend auf dem Schieberegler
        for field, line in self.lines.items():
            line.set_ydata(self.data_buffer[field][-self.current_view_size:])
            line.set_xdata(self.t[-self.current_view_size:])

        self.draw()

    def set_view_size(self, view_size):
        # Setze die Anzahl der Datenpunkte, die angezeigt werden sollen
        self.current_view_size = view_size
        # Plot mit dem neuen View-Bereich aktualisieren
        self.update_plot(self.data_buffer)
