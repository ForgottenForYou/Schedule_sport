import os
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from constants import ICONS_DIR


class FlatButton(QPushButton):
    """Плоская кнопка с иконкой и текстом"""

    def __init__(self, text, icon_name=None, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)

        if icon_name:
            icon_path = os.path.join(ICONS_DIR, f"{icon_name}.png")
            if os.path.exists(icon_path):
                self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))