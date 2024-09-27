import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import Qt


class DtypeConfigurator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        # Feldname und Typ auswählen
        self.fieldname_input = QLineEdit(self)
        self.fieldname_input.setPlaceholderText("Feldname")
        self.fieldtype_selector = QComboBox(self)
        self.fieldtype_selector.addItems(
            ["int32", "float32", "float64", "int16", "int8", "uint8"])

        # Hinzufügen von Elementen zum Layout
        self.layout.addWidget(QLabel("Feldname:"))
        self.layout.addWidget(self.fieldname_input)
        self.layout.addWidget(QLabel("Datentyp:"))
        self.layout.addWidget(self.fieldtype_selector)

        # Button zum Anwenden der Konfiguration
        self.apply_button = QPushButton("dtype anwenden", self)
        self.apply_button.clicked.connect(self.apply_dtype)
        self.layout.addWidget(self.apply_button)

        # Tabelle für den aktuellen dtype
        self.dtype_table = QTableWidget(self)
        # Spalten für Name, Typ, und Checkbox
        self.dtype_table.setColumnCount(3)
        self.dtype_table.setHorizontalHeaderLabels(
            ["Feldname", "Datentyp", "Plotten"])
        self.layout.addWidget(self.dtype_table)

        # Container für dtype-Felder
        self.dtype_fields = []

        self.setLayout(self.layout)

    def apply_dtype(self):
        # Benutzerdefinierte dtype-Konfiguration sammeln
        field_name = self.fieldname_input.text()
        field_type = self.fieldtype_selector.currentText()

        if field_name and field_type:
            # dtype-Feld zur Liste hinzufügen
            self.dtype_fields.append((field_name, field_type))
            self.update_dtype_table()
            print(f"Neues Feld hinzugefügt: ({field_name}, {field_type})")
        else:
            print("Bitte Feldname und Datentyp eingeben.")

    def update_dtype_table(self):
        # Tabelle aktualisieren, um den aktuellen dtype anzuzeigen
        self.dtype_table.setRowCount(len(self.dtype_fields))
        for i, (field_name, field_type) in enumerate(self.dtype_fields):
            # Feldname und Datentyp in die Tabelle einfügen
            self.dtype_table.setItem(i, 0, QTableWidgetItem(field_name))
            self.dtype_table.setItem(i, 1, QTableWidgetItem(field_type))

            # Checkbox hinzufügen, um das Plotten zu steuern
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Unchecked)
            self.dtype_table.setItem(i, 2, checkbox)

    def get_dtype(self):
        # dtype basierend auf der Benutzerkonfiguration erstellen
        dtype = np.dtype(self.dtype_fields)
        print(f"Dynamischer dtype erstellt: {dtype}")
        return dtype

    def get_plot_fields(self):
        # Ermitteln, welche Felder geplottet werden sollen
        plot_fields = []
        for i in range(self.dtype_table.rowCount()):
            if self.dtype_table.item(i, 2).checkState() == Qt.Checked:
                # Feldname zum Plotten
                plot_fields.append(self.dtype_fields[i][0])
        return plot_fields
