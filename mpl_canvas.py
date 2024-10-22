from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.lines = {}  # Ein Dictionary, um die Linien zu speichern
        self.buffer_size = 1000  # Buffer-Größe (basiert auf dem Ring-Buffer)
        self.current_view_size = 100  # Standard-Anzeigebereich

    def init_plot(self, fields):
        """Initialisiert den Plot für die ausgewählten Felder."""
        self.axes.clear()  # Löscht alle bestehenden Linien aus dem Plot
        self.lines = {}  # Leert das Dictionary mit den Linien

        # X-Achse für die Zeit/Index
        self.t = np.linspace(0, self.buffer_size - 1, self.buffer_size)

        # Initialisiere eine leere Linie für jedes Feld
        for field in fields:
            # Initialisiere die Linie nur, wenn sie noch nicht existiert
            if field not in self.lines:
                line, = self.axes.plot([], [], label=field)
                self.lines[field] = line  # Speichere die Linie im Dictionary

        self.axes.legend()  # Zeige die Legende für die ausgewählten Felder an
        self.draw()

    def update_plot(self, data, current_size):
        """Aktualisiert den Plot mit neuen Daten aus dem Ring-Buffer."""
        display_size = min(
            self.current_view_size, current_size)  # Stelle sicher, dass nur vorhandene Daten angezeigt werden
        # Zeige die letzten `display_size` Daten an, X-Achse wird in Sekunden angezeigt
        # 0.1 Sekunden pro Datenpunkt
        time_in_seconds = np.arange(display_size) * 0.1

        # print(data.items())

        for field, new_data in data.items():
            self.lines[field].set_ydata(new_data[-display_size:])
            self.lines[field].set_xdata(time_in_seconds)

        self.axes.relim()  # Aktualisiere die Achsenbegrenzungen
        self.axes.autoscale_view()  # Skalierung automatisch anpassen
        self.draw()  # Aktualisiere den Plot

    def set_view_size(self, view_size):
        """Setze die aktuelle Anzahl der anzuzeigenden Datenpunkte basierend auf dem Slider-Wert."""
        self.current_view_size = view_size
