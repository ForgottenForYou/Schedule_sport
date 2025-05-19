from datetime import datetime
from PyQt5.QtWidgets import (QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QMessageBox, QDialog)
from PyQt5.QtCore import Qt
from widgets.buttons import FlatButton
from widgets.schedule_cell import ScheduleCell
from widgets.schedule_filter import ScheduleFilterPanel
from dialogs import AddScheduleDialog
from constants import DAYS_OF_WEEK, DEFAULT_TIME_SLOTS


class ScheduleGridView(QScrollArea):
    """Сетка расписания с фильтрацией"""

    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWidgetResizable(True)
        self.setObjectName("scheduleGrid")
        self.current_filters = {'group_id': None, 'coach_id': None}

        # Создаем основной виджет для содержимого
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)

        # Добавляем панель фильтров
        self.filter_panel = ScheduleFilterPanel(self.db)
        self.filter_panel.set_filter_changed_callback(self.apply_filters)
        self.content_layout.addWidget(self.filter_panel)

        # Создаем сетку расписания
        self.grid_frame = QFrame()
        self.grid_frame.setObjectName("gridFrame")

        self.grid_layout = QGridLayout(self.grid_frame)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(1)

        # Заголовки дней недели
        days = ["", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

        for col, day in enumerate(days):
            if col == 0:
                # Первая ячейка - пустая (над временем)
                header = QLabel("")
                header.setObjectName("cornerHeader")
            else:
                header = QLabel(day)
                header.setObjectName("dayHeader")
                header.setAlignment(Qt.AlignCenter)

            self.grid_layout.addWidget(header, 0, col)

        # Добавляем временные слоты
        for row, time_slot in enumerate(DEFAULT_TIME_SLOTS, 1):
            time_label = QLabel(time_slot)
            time_label.setObjectName("timeLabel")
            time_label.setAlignment(Qt.AlignCenter)

            self.grid_layout.addWidget(time_label, row, 0)

            # Добавляем пустые ячейки для каждого дня недели
            for col in range(1, 8):
                empty_cell = QFrame()
                empty_cell.setObjectName("emptyCell")
                self.grid_layout.addWidget(empty_cell, row, col)

        self.content_layout.addWidget(self.grid_frame)

        # Добавляем кнопки
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.setSpacing(10)

        add_button = FlatButton("Добавить занятие", "add")
        add_button.setObjectName("addButton")
        add_button.clicked.connect(self.add_schedule_item)

        export_button = FlatButton("Экспортировать расписание", "export")
        export_button.setObjectName("exportButton")
        export_button.clicked.connect(self.export_schedule)

        button_layout.addWidget(add_button)
        button_layout.addStretch()
        button_layout.addWidget(export_button)

        self.content_layout.addLayout(button_layout)
        self.setWidget(self.content_widget)

        # Загружаем расписание
        self.load_schedule()

    def apply_filters(self, group_id, coach_id):
        """Применить фильтры и обновить расписание"""
        self.current_filters['group_id'] = group_id
        self.current_filters['coach_id'] = coach_id
        self.load_schedule()

    def load_schedule(self):
        # Сначала очищаем все ячейки, кроме заголовков
        for row in range(1, len(DEFAULT_TIME_SLOTS) + 1):
            for col in range(1, 8):  # Дни недели (1-7)
                item = self.grid_layout.itemAtPosition(row, col)
                if item:
                    widget = item.widget()
                    if widget and widget.objectName() != "emptyCell":
                        self.grid_layout.removeItem(item)
                        widget.deleteLater()

                        # Создаем новую пустую ячейку
                        empty_cell = QFrame()
                        empty_cell.setObjectName("emptyCell")
                        self.grid_layout.addWidget(empty_cell, row, col)

        # Загружаем расписание из базы данных с применением фильтров
        all_schedule = self.db.get_all_schedule_filtered(
            self.current_filters['group_id'],
            self.current_filters['coach_id']
        )

        # Распределяем занятия по сетке
        for item in all_schedule:
            item_id, day_of_week, start_time, end_time, group_name, coach_name, location = item

            # Определяем, в какую ячейку поместить занятие
            col = day_of_week + 1  # +1 потому что первый столбец - это время

            # Находим строку (временной слот)
            row = -1
            for i, time_slot in enumerate(DEFAULT_TIME_SLOTS, 1):
                slot_start, slot_end = time_slot.split('-')
                if start_time >= slot_start and end_time <= slot_end:
                    row = i
                    break

            if row > 0:
                # Удаляем пустую ячейку
                item = self.grid_layout.itemAtPosition(row, col)
                if item:
                    widget = item.widget()
                    self.grid_layout.removeItem(item)
                    widget.deleteLater()

                # Создаем ячейку с занятием
                cell = ScheduleCell(item_id, group_name, coach_name, location)
                cell.customContextMenuRequested.connect(
                    lambda pos, r=row, c=col, id=item_id: self.show_context_menu(pos, r, c, id))

                self.grid_layout.addWidget(cell, row, col)

    def show_context_menu(self, pos, row, col, item_id):
        menu = QDialog.createStandardContextMenu(self.sender())
        menu.addSeparator()

        edit_action = menu.addAction("Редактировать")
        delete_action = menu.addAction("Удалить")

        cell = self.sender()
        global_pos = cell.mapToGlobal(pos)

        action = menu.exec_(global_pos)

        if action == edit_action:
            self.edit_schedule_item(item_id)
        elif action == delete_action:
            reply = QMessageBox.question(
                self, 'Подтверждение',
                "Вы уверены, что хотите удалить это занятие?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.db.delete_schedule_item(item_id)
                self.load_schedule()

    def add_schedule_item(self):
        coaches = self.db.get_all_coaches()
        groups = self.db.get_all_groups()

        if not coaches:
            QMessageBox.warning(self, "Предупреждение", "Сначала добавьте хотя бы одного тренера!")
            return

        if not groups:
            QMessageBox.warning(self, "Предупреждение", "Сначала добавьте хотя бы одну группу!")
            return

        dialog = AddScheduleDialog(self.db, self)

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

    def edit_schedule_item(self, item_id):
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

    def export_schedule(self):
        try:
            # Экспорт в текстовый файл
            with open("schedule_export.txt", "w", encoding="utf-8") as f:
                current_date = datetime.now().strftime("%d.%m.%Y")
                f.write(f"РАСПИСАНИЕ ЗАНЯТИЙ СПОРТИВНОЙ ШКОЛЫ\n")
                f.write(f"Дата составления: {current_date}\n")
                f.write("=" * 80 + "\n\n")

                for time_slot in DEFAULT_TIME_SLOTS:
                    f.write(f"\n{time_slot}\n")
                    f.write("-" * 80 + "\n")

                    for day_idx, day_name in enumerate(DAYS_OF_WEEK):
                        f.write(f"{day_name}:\n")

                        # Найти занятия для этого временного слота и дня недели
                        found = False
                        schedule_items = self.db.get_schedule_for_day(day_idx)
                        for item_id, start_time, end_time, group_name, coach_name, location in schedule_items:
                            slot_start, slot_end = time_slot.split('-')
                            if start_time >= slot_start and end_time <= slot_end:
                                f.write(f"  * Группа: {group_name} | Тренер: {coach_name} | Место: {location}\n")
                                found = True

                        if not found:
                            f.write("  * Нет занятий\n")

            QMessageBox.information(self, "Экспорт", "Расписание успешно экспортировано в файл schedule_export.txt")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при экспорте: {str(e)}")