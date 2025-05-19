from PyQt5.QtWidgets import (QDialog, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFormLayout, QLineEdit, QComboBox, QTimeEdit)
from PyQt5.QtCore import Qt, QTime


class StyledDialog(QDialog):
    """Базовый класс для стилизованных диалогов"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Основной контейнер с рамкой и тенью
        self.container = QFrame(self)
        self.container.setObjectName("dialogContainer")

        # Заголовок диалога
        self.title_bar = QFrame(self.container)
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(40)

        self.title_label = QLabel("Диалог", self.title_bar)
        self.title_label.setObjectName("titleLabel")

        self.close_button = QPushButton("×", self.title_bar)
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.reject)

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.close_button)

        # Содержимое диалога
        self.content_frame = QFrame(self.container)
        self.content_frame.setObjectName("contentFrame")

        # Кнопки
        self.button_frame = QFrame(self.container)
        self.button_frame.setObjectName("buttonFrame")

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setObjectName("saveButton")
        self.save_button.clicked.connect(self.accept)

        buttons_layout = QHBoxLayout(self.button_frame)
        buttons_layout.setContentsMargins(10, 5, 10, 10)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)

        # Основной layout
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.title_bar)
        container_layout.addWidget(self.content_frame)
        container_layout.addWidget(self.button_frame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.container)

    def setTitle(self, title):
        self.title_label.setText(title)
        self.setWindowTitle(title)


class AddCoachDialog(StyledDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Добавить тренера")
        self.setFixedWidth(400)

        layout = QFormLayout(self.content_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введите ФИО тренера")
        self.name_edit.setMinimumHeight(35)

        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Введите номер телефона")
        self.phone_edit.setMinimumHeight(35)

        self.specialization_edit = QLineEdit()
        self.specialization_edit.setPlaceholderText("Введите специализацию")
        self.specialization_edit.setMinimumHeight(35)

        layout.addRow(QLabel("<b>ФИО:</b>"), self.name_edit)
        layout.addRow(QLabel("<b>Телефон:</b>"), self.phone_edit)
        layout.addRow(QLabel("<b>Специализация:</b>"), self.specialization_edit)

    def get_coach_data(self):
        return {
            'name': self.name_edit.text(),
            'phone': self.phone_edit.text(),
            'specialization': self.specialization_edit.text()
        }


class AddGroupDialog(StyledDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Добавить группу")
        self.setFixedWidth(400)

        layout = QFormLayout(self.content_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введите название группы")
        self.name_edit.setMinimumHeight(35)

        self.age_range_edit = QLineEdit()
        self.age_range_edit.setPlaceholderText("Например: 10-12 лет")
        self.age_range_edit.setMinimumHeight(35)

        self.sport_type_edit = QLineEdit()
        self.sport_type_edit.setPlaceholderText("Введите вид спорта")
        self.sport_type_edit.setMinimumHeight(35)

        layout.addRow(QLabel("<b>Название группы:</b>"), self.name_edit)
        layout.addRow(QLabel("<b>Возрастной диапазон:</b>"), self.age_range_edit)
        layout.addRow(QLabel("<b>Вид спорта:</b>"), self.sport_type_edit)

    def get_group_data(self):
        return {
            'name': self.name_edit.text(),
            'age_range': self.age_range_edit.text(),
            'sport_type': self.sport_type_edit.text()
        }


class AddScheduleDialog(StyledDialog):
    def __init__(self, db, parent=None, edit_mode=False, schedule_id=None):
        super().__init__(parent)
        self.db = db
        self.edit_mode = edit_mode
        self.schedule_id = schedule_id

        if edit_mode:
            self.setTitle("Редактировать занятие")
        else:
            self.setTitle("Добавить занятие")

        self.setFixedWidth(500)

        layout = QFormLayout(self.content_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # День недели
        self.day_combo = QComboBox()
        self.day_combo.setMinimumHeight(35)
        from constants import DAYS_OF_WEEK
        for day in DAYS_OF_WEEK:
            self.day_combo.addItem(day)

        # Время начала и окончания
        time_layout = QHBoxLayout()

        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm")
        self.start_time_edit.setTime(QTime(8, 0))
        self.start_time_edit.setMinimumHeight(35)

        time_separator = QLabel("—")
        time_separator.setAlignment(Qt.AlignCenter)

        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm")
        self.end_time_edit.setTime(QTime(9, 0))
        self.end_time_edit.setMinimumHeight(35)

        time_layout.addWidget(self.start_time_edit)
        time_layout.addWidget(time_separator)
        time_layout.addWidget(self.end_time_edit)

        # Группа и тренер
        self.group_combo = QComboBox()
        self.group_combo.setMinimumHeight(35)
        groups = self.db.get_all_groups()
        for group_id, group_name in groups:
            self.group_combo.addItem(group_name, group_id)

        self.coach_combo = QComboBox()
        self.coach_combo.setMinimumHeight(35)
        coaches = self.db.get_all_coaches()
        for coach_id, coach_name in coaches:
            self.coach_combo.addItem(coach_name, coach_id)

        # Место проведения
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Введите место проведения занятия")
        self.location_edit.setMinimumHeight(35)

        layout.addRow(QLabel("<b>День недели:</b>"), self.day_combo)
        layout.addRow(QLabel("<b>Время занятия:</b>"), time_layout)
        layout.addRow(QLabel("<b>Группа:</b>"), self.group_combo)
        layout.addRow(QLabel("<b>Тренер:</b>"), self.coach_combo)
        layout.addRow(QLabel("<b>Место проведения:</b>"), self.location_edit)

        if edit_mode and schedule_id:
            self.load_schedule_data()

    def load_schedule_data(self):
        data = self.db.get_schedule_item(self.schedule_id)
        if data:
            day_of_week, start_time, end_time, group_id, coach_id, location = data

            self.day_combo.setCurrentIndex(day_of_week)

            start_time_obj = QTime.fromString(start_time, "HH:mm")
            self.start_time_edit.setTime(start_time_obj)

            end_time_obj = QTime.fromString(end_time, "HH:mm")
            self.end_time_edit.setTime(end_time_obj)

            # Найти индекс группы и тренера в комбо-боксах
            group_index = self.group_combo.findData(group_id)
            if group_index >= 0:
                self.group_combo.setCurrentIndex(group_index)

            coach_index = self.coach_combo.findData(coach_id)
            if coach_index >= 0:
                self.coach_combo.setCurrentIndex(coach_index)

            self.location_edit.setText(location)

    def get_schedule_data(self):
        day_of_week = self.day_combo.currentIndex()
        start_time = self.start_time_edit.time().toString("HH:mm")
        end_time = self.end_time_edit.time().toString("HH:mm")
        group_id = self.group_combo.currentData()
        coach_id = self.coach_combo.currentData()
        location = self.location_edit.text()

        return {
            'day_of_week': day_of_week,
            'start_time': start_time,
            'end_time': end_time,
            'group_id': group_id,
            'coach_id': coach_id,
            'location': location
        }