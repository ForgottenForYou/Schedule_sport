from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QFrame
from views.schedule_list import ScheduleListView
from views.schedule_grid import ScheduleGridView


class ScheduleTab(QWidget):
    """Вкладка расписания с переключением между видом списка и сеткой"""

    def __init__(self, db):
        super().__init__()
        self.db = db

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Заголовок
        header_layout = QHBoxLayout()

        header = QLabel("Расписание занятий")
        header.setObjectName("pageHeader")
        header_layout.addWidget(header)

        # Переключатели вида расписания
        view_frame = QFrame()
        view_frame.setObjectName("viewSwitcher")
        view_layout = QHBoxLayout(view_frame)
        view_layout.setContentsMargins(10, 0, 10, 0)
        view_layout.setSpacing(0)

        self.list_button = QPushButton("Список")
        self.list_button.setObjectName("viewButton")
        self.list_button.setCheckable(True)
        self.list_button.setChecked(True)
        self.list_button.clicked.connect(lambda: self.switch_view(0))

        self.grid_button = QPushButton("Сетка")
        self.grid_button.setObjectName("viewButton")
        self.grid_button.setCheckable(True)
        self.grid_button.clicked.connect(lambda: self.switch_view(1))

        view_layout.addWidget(self.list_button)
        view_layout.addWidget(self.grid_button)

        header_layout.addStretch()
        header_layout.addWidget(view_frame)

        layout.addLayout(header_layout)

        # Стек с видами расписания
        self.view_stack = QStackedWidget()

        # Вид списка
        self.list_view = ScheduleListView(self.db)
        self.view_stack.addWidget(self.list_view)

        # Вид сетки
        self.grid_view = ScheduleGridView(self.db)
        self.view_stack.addWidget(self.grid_view)

        layout.addWidget(self.view_stack)

    def switch_view(self, index):
        self.view_stack.setCurrentIndex(index)

        if index == 0:
            self.list_button.setChecked(True)
            self.grid_button.setChecked(False)
        else:
            self.list_button.setChecked(False)
            self.grid_button.setChecked(True)