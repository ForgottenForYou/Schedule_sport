from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from widgets.buttons import FlatButton
from dialogs import AddCoachDialog
from database import Database


class CoachesTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Заголовок
        header = QLabel("Тренеры")
        header.setObjectName("pageHeader")
        layout.addWidget(header)

        # Кнопка добавления тренера
        add_button = FlatButton("Добавить тренера", "add_user")
        add_button.setObjectName("addButton")
        add_button.clicked.connect(self.add_coach)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Таблица тренеров
        self.coaches_table = QTableWidget()
        self.coaches_table.setObjectName("dataTable")
        self.coaches_table.setColumnCount(3)
        self.coaches_table.setHorizontalHeaderLabels(["ФИО", "Телефон", "Специализация"])
        self.coaches_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.coaches_table.setAlternatingRowColors(True)
        self.coaches_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.coaches_table.setSelectionMode(QTableWidget.SingleSelection)
        self.coaches_table.verticalHeader().setVisible(False)

        layout.addWidget(self.coaches_table)
        self.load_coaches()

    def load_coaches(self):
        self.db.cursor.execute('SELECT name, phone, specialization FROM coaches')
        coaches = self.db.cursor.fetchall()

        self.coaches_table.setRowCount(len(coaches))
        for i, (name, phone, specialization) in enumerate(coaches):
            self.coaches_table.setItem(i, 0, QTableWidgetItem(name))
            self.coaches_table.setItem(i, 1, QTableWidgetItem(phone))
            self.coaches_table.setItem(i, 2, QTableWidgetItem(specialization))

    def add_coach(self):
        dialog = AddCoachDialog(self)
        if dialog.exec_():
            coach_data = dialog.get_coach_data()
            if not coach_data['name']:
                QMessageBox.warning(self, "Предупреждение", "Имя тренера не может быть пустым!")
                return

            self.db.add_coach(coach_data['name'], coach_data['phone'], coach_data['specialization'])
            self.load_coaches()