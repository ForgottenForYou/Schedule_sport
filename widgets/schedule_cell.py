from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class ScheduleCell(QFrame):
    """Ячейка расписания с информацией о занятии"""

    def __init__(self, schedule_id, group_name, coach_name, location, parent=None):
        super().__init__(parent)
        self.schedule_id = schedule_id
        self.setObjectName("scheduleCell")
        self.setFixedHeight(100)
        self.setMinimumWidth(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)

        group_label = QLabel(group_name)
        group_label.setObjectName("cellGroupLabel")
        group_label.setAlignment(Qt.AlignCenter)

        coach_label = QLabel(coach_name)
        coach_label.setObjectName("cellCoachLabel")
        coach_label.setAlignment(Qt.AlignCenter)

        location_label = QLabel(location)
        location_label.setObjectName("cellLocationLabel")
        location_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(group_label)
        layout.addWidget(coach_label)
        layout.addWidget(location_label)

        # Создаем контекстное меню
        self.setContextMenuPolicy(Qt.CustomContextMenu)