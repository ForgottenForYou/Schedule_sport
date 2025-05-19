from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from widgets.buttons import FlatButton
from dialogs import AddGroupDialog


class GroupsTab(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Заголовок
        header = QLabel("Группы")
        header.setObjectName("pageHeader")
        layout.addWidget(header)

        # Кнопка добавления группы
        add_button = FlatButton("Добавить группу", "add_group")
        add_button.setObjectName("addButton")
        add_button.clicked.connect(self.add_group)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Таблица групп
        self.groups_table = QTableWidget()
        self.groups_table.setObjectName("dataTable")
        self.groups_table.setColumnCount(3)
        self.groups_table.setHorizontalHeaderLabels(["Название", "Возраст", "Вид спорта"])
        self.groups_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.groups_table.setAlternatingRowColors(True)
        self.groups_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.groups_table.setSelectionMode(QTableWidget.SingleSelection)
        self.groups_table.verticalHeader().setVisible(False)

        layout.addWidget(self.groups_table)
        self.load_groups()

    def load_groups(self):
        self.db.cursor.execute('SELECT name, age_range, sport_type FROM groups')
        groups = self.db.cursor.fetchall()

        self.groups_table.setRowCount(len(groups))
        for i, (name, age_range, sport_type) in enumerate(groups):
            self.groups_table.setItem(i, 0, QTableWidgetItem(name))
            self.groups_table.setItem(i, 1, QTableWidgetItem(age_range))
            self.groups_table.setItem(i, 2, QTableWidgetItem(sport_type))

    def add_group(self):
        dialog = AddGroupDialog(self)
        if dialog.exec_():
            group_data = dialog.get_group_data()
            if not group_data['name']:
                QMessageBox.warning(self, "Предупреждение", "Название группы не может быть пустым!")
                return

            self.db.add_group(group_data['name'], group_data['age_range'], group_data['sport_type'])
            self.load_groups()