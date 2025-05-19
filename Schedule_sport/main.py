import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from database import Database
from styles import get_application_styles
from views.schedule import ScheduleTab
from views.coaches import CoachesTab
from views.groups import GroupsTab
from constants import ICONS_DIR


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()

        self.setWindowTitle("Расписание спортивной школы")
        self.setGeometry(100, 100, 1200, 800)

        # Устанавливаем иконку приложения, если она есть
        icon_path = os.path.join(ICONS_DIR, "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Создаем шапку
        header = QFrame()
        header.setObjectName("appHeader")
        header.setFixedHeight(70)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)

        # Добавляем логотип и название
        logo_label = QLabel("🏆")
        logo_label.setObjectName("appLogo")
        logo_label.setFont(QFont("Arial", 24))

        title_label = QLabel("Расписание спортивной школы")
        title_label.setObjectName("appTitle")

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        main_layout.addWidget(header)

        # Создаем содержимое
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")

        # Создаем вкладки
        self.schedule_tab = ScheduleTab(self.db)
        self.coaches_tab = CoachesTab(self.db)
        self.groups_tab = GroupsTab(self.db)

        # Добавляем вкладки
        self.tabs.addTab(self.schedule_tab, "Расписание")
        self.tabs.addTab(self.coaches_tab, "Тренеры")
        self.tabs.addTab(self.groups_tab, "Группы")

        content_layout.addWidget(self.tabs)

        main_layout.addWidget(content_container)

    def apply_styles(self):
        # Применяем стили CSS ко всему приложению
        self.setStyleSheet(get_application_styles())

    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())