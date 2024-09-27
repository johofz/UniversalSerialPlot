def get_dark_theme():
    return """
        QMainWindow {
            background-color: #2b2b2b;
        }
        QTabWidget::pane {
            border: 1px solid #555;
            background-color: #2b2b2b;
        }
        QWidget {
            font-family: Arial;
            font-size: 12px;
            color: #c5c6c7;
        }
        QPushButton {
            background-color: #3a3f44;
            color: #c5c6c7;
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #555;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #4b535a;
        }
        QSlider::groove:horizontal {
            background-color: #555;
            height: 8px;
            border-radius: 4px;
        }
        QSlider::handle:horizontal {
            background: #888;
            border: 1px solid #333;
            width: 20px;
            margin: -5px 0;
            border-radius: 5px;
        }
        QLabel {
            color: #c5c6c7;
        }
        QTabBar::tab {
            background: #3a3f44;
            color: #c5c6c7;
            padding: 10px;
            border: 1px solid #555;
        }
        QTabBar::tab:selected {
            background: #555;
            color: white;
        }
    """
