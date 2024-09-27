import numpy as np


class RingBuffer:
    def __init__(self, size, dtype=np.float32):
        self.size = size  # Maximale Größe des Buffers
        self.data = np.zeros(size, dtype=dtype)
        self.index = 0
        self.is_full = False

    def append(self, value):
        """Fügt einen neuen Wert zum Buffer hinzu."""
        self.data[self.index] = value
        self.index = (self.index + 1) % self.size
        if self.index == 0:
            self.is_full = True

    def get(self):
        """Gibt die Daten im Buffer in der richtigen Reihenfolge zurück."""
        if self.is_full:
            return np.concatenate((self.data[self.index:], self.data[:self.index]))
        else:
            return self.data[:self.index]
