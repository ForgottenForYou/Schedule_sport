from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton
from database import Database


class ScheduleFilterPanel(QWidget):
    """Панель фильтров для расписания"""

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.filter_changed_callback = None

        self.setObjectName("filterPanel")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(15)

        # Метка фильтра
        filter_label = QLabel("Фильтр:")
        filter_label.setObjectName("filterLabel")

        # Выбор группы
        group_layout = QHBoxLayout()
        group_label = QLabel("Группа:")
        self.group_combo = QComboBox()
        self.group_combo.setMinimumWidth(150)
        self.group_combo.addItem("Все группы", None)

        groups = self.db.get_all_groups()
        for group_id, group_name in groups:
            self.group_combo.addItem(group_name, group_id)

        self.group_combo.currentIndexChanged.connect(self.on_filter_changed)

        group_layout.addWidget(group_label)
        group_layout.addWidget(self.group_combo)

        # Выбор тренера
        coach_layout = QHBoxLayout()
        coach_label = QLabel("Тренер:")
        self.coach_combo = QComboBox()
        self.coach_combo.setMinimumWidth(200)
        self.coach_combo.addItem("Все тренеры", None)

        coaches = self.db.get_all_coaches()
        for coach_id, coach_name in coaches:
            self.coach_combo.addItem(coach_name, coach_id)

        self.coach_combo.currentIndexChanged.connect(self.on_filter_changed)

        coach_layout.addWidget(coach_label)
        coach_layout.addWidget(self.coach_combo)

        # Кнопка сброса фильтров
        self.reset_button = QPushButton("Сбросить")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.reset_filters)

        layout.addWidget(filter_label)
        layout.addLayout(group_layout)
        layout.addLayout(coach_layout)
        layout.addWidget(self.reset_button)
        layout.addStretch()

    def set_filter_changed_callback(self, callback):
        """Установка функции обратного вызова при изменении фильтра"""
        self.filter_changed_callback = callback

    def on_filter_changed(self):
        """Вызывается при изменении любого фильтра"""
        if self.filter_changed_callback:
            group_id = self.group_combo.currentData()
            coach_id = self.coach_combo.currentData()
            self.filter_changed_callback(group_id, coach_id)

    def reset_filters(self):
        """Сбросить все фильтры"""
        self.group_combo.setCurrentIndex(0)  # "Все группы"
        self.coach_combo.setCurrentIndex(0)  # "Все тренеры"

    def get_current_filters(self):
        """Получить текущие значения фильтров"""
        return {
            'group_id': self.group_combo.currentData(),
            'coach_id': self.coach_combo.currentData()
        }