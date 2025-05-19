from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog)
from PyQt5.QtCore import Qt
from widgets.buttons import FlatButton
from widgets.schedule_filter import ScheduleFilterPanel
from dialogs import AddScheduleDialog
from constants import DAYS_OF_WEEK


class ScheduleListView(QWidget):
    """Отображение расписания в виде списка по дням недели с фильтрацией"""

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.current_day = 0  # Понедельник по умолчанию
        self.current_filters = {'group_id': None, 'coach_id': None}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Добавляем панель фильтров
        self.filter_panel = ScheduleFilterPanel(self.db)
        self.filter_panel.set_filter_changed_callback(self.apply_filters)
        layout.addWidget(self.filter_panel)

        # Панель выбора дня
        self.day_buttons = []
        day_selector = QWidget()
        day_selector.setObjectName("daySelector")
        day_layout = QHBoxLayout(day_selector)
        day_layout.setContentsMargins(0, 0, 0, 0)
        day_layout.setSpacing(1)

        # Создаем кнопки для дней недели
        for i, day in enumerate(DAYS_OF_WEEK):
            day_button = QPushButton(day)
            day_button.setObjectName("dayButton")
            day_button.setCheckable(True)
            day_button.clicked.connect(lambda checked, day_idx=i: self.change_day(day_idx))
            if i == self.current_day:
                day_button.setChecked(True)
            self.day_buttons.append(day_button)
            day_layout.addWidget(day_button)

        day_layout.addStretch()
        layout.addWidget(day_selector)

        # Содержимое расписания
        schedule_container = QWidget()
        schedule_container.setObjectName("scheduleContainer")
        schedule_layout = QVBoxLayout(schedule_container)
        schedule_layout.setContentsMargins(0, 0, 0, 0)
        schedule_layout.setSpacing(15)

        # Заголовок текущего дня
        self.current_day_label = QLabel(DAYS_OF_WEEK[self.current_day])
        self.current_day_label.setObjectName("currentDayLabel")
        self.current_day_label.setAlignment(Qt.AlignCenter)
        schedule_layout.addWidget(self.current_day_label)

        # Таблица расписания
        self.schedule_table = QTableWidget()
        self.schedule_table.setObjectName("scheduleTable")
        self.schedule_table.setColumnCount(5)
        self.schedule_table.setHorizontalHeaderLabels(["ID", "Время", "Группа", "Тренер", "Место"])
        self.schedule_table.setColumnHidden(0, True)  # Скрываем колонку ID

        # Настройка ширины колонок
        self.schedule_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.schedule_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.schedule_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.schedule_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

        self.schedule_table.setAlternatingRowColors(True)
        self.schedule_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.schedule_table.setSelectionMode(QTableWidget.SingleSelection)
        self.schedule_table.verticalHeader().setVisible(False)
        self.schedule_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Контекстное меню для таблицы
        self.schedule_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.schedule_table.customContextMenuRequested.connect(self.show_context_menu)
        self.schedule_table.cellDoubleClicked.connect(self.edit_schedule_item)

        schedule_layout.addWidget(self.schedule_table)

        # Кнопки действий
        action_layout = QHBoxLayout()

        add_button = FlatButton("Добавить занятие", "add")
        add_button.setObjectName("addButton")
        add_button.clicked.connect(self.add_schedule_item)

        export_button = FlatButton("Экспортировать расписание", "export")
        export_button.setObjectName("exportButton")
        export_button.clicked.connect(self.export_schedule)

        action_layout.addWidget(add_button)
        action_layout.addStretch()
        action_layout.addWidget(export_button)

        schedule_layout.addLayout(action_layout)

        layout.addWidget(schedule_container)

        self.load_schedule()

    def change_day(self, day_index):
        if day_index == self.current_day:
            return

        self.current_day = day_index

        # Обновляем состояние кнопок
        for i, button in enumerate(self.day_buttons):
            button.setChecked(i == day_index)

        # Обновляем заголовок
        self.current_day_label.setText(DAYS_OF_WEEK[day_index])

        # Загружаем расписание для выбранного дня
        self.load_schedule()

    def apply_filters(self, group_id, coach_id):
        """Применить фильтры и обновить расписание"""
        self.current_filters['group_id'] = group_id
        self.current_filters['coach_id'] = coach_id
        self.load_schedule()

    def load_schedule(self):
        # Используем новый метод с фильтрацией
        schedule_items = self.db.get_schedule_for_day_filtered(
            self.current_day,
            self.current_filters['group_id'],
            self.current_filters['coach_id']
        )

        self.schedule_table.setRowCount(len(schedule_items))
        for i, (item_id, start_time, end_time, group_name, coach_name, location) in enumerate(schedule_items):
            self.schedule_table.setItem(i, 0, QTableWidgetItem(str(item_id)))

            # Время в формате 08:00 — 09:30
            time_item = QTableWidgetItem(f"{start_time} — {end_time}")
            time_item.setTextAlignment(Qt.AlignCenter)
            self.schedule_table.setItem(i, 1, time_item)

            group_item = QTableWidgetItem(group_name)
            self.schedule_table.setItem(i, 2, group_item)

            coach_item = QTableWidgetItem(coach_name)
            self.schedule_table.setItem(i, 3, coach_item)

            location_item = QTableWidgetItem(location)
            self.schedule_table.setItem(i, 4, location_item)

    def add_schedule_item(self):
        # Проверим, есть ли тренеры и группы
        coaches = self.db.get_all_coaches()
        groups = self.db.get_all_groups()

        if not coaches:
            QMessageBox.warning(self, "Предупреждение", "Сначала добавьте хотя бы одного тренера!")
            return

        if not groups:
            QMessageBox.warning(self, "Предупреждение", "Сначала добавьте хотя бы одну группу!")
            return

        dialog = AddScheduleDialog(self.db, self)
        dialog.day_combo.setCurrentIndex(self.current_day)

        if dialog.exec_():
            data = dialog.get_schedule_data()
            self.db.add_schedule(
                data['day_of_week'],
                data['start_time'],
                data['end_time'],
                data['group_id'],
                data['coach_id'],
                data['location']
            )
            self.load_schedule()

    def edit_schedule_item(self, row, column):
        item_id = int(self.schedule_table.item(row, 0).text())

        dialog = AddScheduleDialog(self.db, self, edit_mode=True, schedule_id=item_id)

        if dialog.exec_():
            data = dialog.get_schedule_data()
            self.db.update_schedule_item(
                item_id,
                data['day_of_week'],
                data['start_time'],
                data['end_time'],
                data['group_id'],
                data['coach_id'],
                data['location']
            )
            self.load_schedule()

    def show_context_menu(self, position):
        selected_rows = self.schedule_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        item_id = int(self.schedule_table.item(row, 0).text())

        menu = QDialog.createStandardContextMenu(self.schedule_table)
        menu.addSeparator()

        edit_action = menu.addAction("Редактировать")
        delete_action = menu.addAction("Удалить")

        action = menu.exec_(self.schedule_table.mapToGlobal(position))

        if action == edit_action:
            self.edit_schedule_item(row, 0)
        elif action == delete_action:
            reply = QMessageBox.question(
                self, 'Подтверждение',
                "Вы уверены, что хотите удалить это занятие?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db.delete_schedule_item(item_id)
                self.load_schedule()

    def export_schedule(self):
        try:
            # Экспорт в текстовый файл
            with open("schedule_export.txt", "w", encoding="utf-8") as f:
                current_date = datetime.now().strftime("%d.%m.%Y")
                f.write(f"РАСПИСАНИЕ ЗАНЯТИЙ СПОРТИВНОЙ ШКОЛЫ\n")
                f.write(f"Дата составления: {current_date}\n")
                f.write("=" * 80 + "\n\n")

                for day_idx, day_name in enumerate(DAYS_OF_WEEK):
                    f.write(f"\n{day_name.upper()}\n")
                    f.write("-" * 80 + "\n")

                    schedule_items = self.db.get_schedule_for_day(day_idx)
                    if schedule_items:
                        for item_id, start_time, end_time, group_name, coach_name, location in schedule_items:
                            f.write(
                                f"{start_time} - {end_time} | Группа: {group_name} | Тренер: {coach_name} | Место: {location}\n")
                    else:
                        f.write("Нет занятий\n")

            QMessageBox.information(self, "Экспорт", "Расписание успешно экспортировано в файл schedule_export.txt")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")