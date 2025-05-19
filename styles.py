def get_application_styles():
    """Возвращает CSS стили для всего приложения"""
    return """
    /* Основные цвета */
    * {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
    }

    QMainWindow, QDialog {
        background-color: #F8F9FA;
    }

    /* Шапка приложения */
    #appHeader {
        background-color: #26A69A;
        color: white;
    }

    #appLogo {
        color: white;
        font-size: 24px;
        padding: 10px;
    }

    #appTitle {
        color: white;
        font-size: 22px;
        font-weight: bold;
    }

    /* Вкладки */
    QTabWidget::pane {
        border: none;
        background-color: #F8F9FA;
    }

QTabBar::tab {
        background-color: #F8F9FA;
        color: #6c757d;
        border: none;
        padding: 12px 16px;
        margin-right: 4px;
        margin-bottom: -1px;
    }
    
    QTabBar::tab:selected {
        color: #26A69A;
        border-bottom: 2px solid #26A69A;
    }
    
    /* Переключатель вида расписания */
    #viewSwitcher {
        background-color: #e9ecef;
        border-radius: 20px;
        max-height: 36px;
    }
    
    #viewButton {
        background-color: transparent;
        color: #495057;
        border: none;
        border-radius: 18px;
        padding: 6px 12px;
        min-width: 80px;
    }
    
    #viewButton:checked {
        background-color: #26A69A;
        color: white;
    }
    
    /* Заголовки страниц */
    #pageHeader {
        color: #212529;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    /* Селектор дней */
    #daySelector {
        background-color: #f8f9fa;
        border-radius: 4px;
    }
    
    #dayButton {
        background-color: transparent;
        color: #495057;
        border: none;
        border-radius: 4px;
        padding: 8px 12px;
    }
    
    #dayButton:checked {
        background-color: #26A69A;
        color: white;
    }
    
    #dayButton:hover:!checked {
        background-color: #e9ecef;
    }
    
    #currentDayLabel {
        font-size: 18px;
        font-weight: bold;
        color: #212529;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 4px;
    }
    
    /* Панель фильтров */
    #filterPanel {
        background-color: #f8f9fa;
        border-radius: 4px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    #filterLabel {
        font-weight: bold;
        color: #495057;
    }
    
    #resetButton {
        background-color: #e9ecef;
        color: #495057;
        border: 1px solid #ced4da;
        padding: 6px 12px;
        font-weight: normal;
    }
    
    #resetButton:hover {
        background-color: #dee2e6;
    }
    
    /* Кнопки */
    QPushButton {
        border: none;
        padding: 10px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    #addButton {
        background-color: #4CAF50;
        color: white;
    }
    
    #addButton:hover {
        background-color: #43A047;
    }
    
    #addButton:pressed {
        background-color: #388E3C;
    }
    
    #exportButton {
        background-color: #2196F3;
        color: white;
    }
    
    #exportButton:hover {
        background-color: #1E88E5;
    }
    
    #exportButton:pressed {
        background-color: #1976D2;
    }
    
    /* Таблицы */
    QTableWidget {
        gridline-color: #e9ecef;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        background-color: white;
    }
    
    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid #e9ecef;
    }
    
    QTableWidget::item:selected {
        background-color: #e3f2fd;
        color: #000;
    }
    
    QHeaderView::section {
        background-color: #f8f9fa;
        padding: 10px;
        border: none;
        border-bottom: 1px solid #dee2e6;
        color: #495057;
        font-weight: bold;
    }
    
    /* Сетка расписания */
    #gridFrame {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
    }
    
    #cornerHeader {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        font-weight: bold;
        padding: 10px;
        min-width: 80px;
        min-height: 50px;
    }
    
    #dayHeader {
        background-color: #26A69A;
        color: white;
        border: 1px solid #dee2e6;
        font-weight: bold;
        padding: 10px;
        min-height: 50px;
    }
    
    #timeLabel {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        font-weight: bold;
        padding: 10px;
        min-width: 80px;
    }
    
    #emptyCell {
        background-color: white;
        border: 1px solid #dee2e6;
        min-height: 80px;
    }
    
    #scheduleCell {
        background-color: #e3f2fd;
        border: 1px solid #bbdefb;
        border-radius: 4px;
        padding: 5px;
    }
    
    #cellGroupLabel {
        font-weight: bold;
        color: #1565C0;
        font-size: 14px;
    }
    
    #cellCoachLabel {
        color: #212529;
    }
    
    #cellLocationLabel {
        color: #6c757d;
        font-style: italic;
    }
    
    /* Расписание */
    #scheduleContainer {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
    }
    
    #scheduleTable {
        margin-top: 10px;
    }
    
    /* Диалоги */
    #dialogContainer {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    #titleBar {
        background-color: #26A69A;
        color: white;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }
    
    #titleLabel {
        font-weight: bold;
        font-size: 16px;
    }
    
    #closeButton {
        background-color: transparent;
        color: white;
        font-size: 20px;
        font-weight: bold;
        border-radius: 15px;
    }
    
    #closeButton:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    #contentFrame {
        background-color: white;
    }
    
    #buttonFrame {
        background-color: #f8f9fa;
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        border-top: 1px solid #e9ecef;
    }
    
    #cancelButton {
        background-color: #f8f9fa;
        color: #6c757d;
        border: 1px solid #dee2e6;
        padding: 8px 16px;
    }
    
    #saveButton {
        background-color: #26A69A;
        color: white;
        padding: 8px 16px;
    }
    
    /* Поля ввода */
    QLineEdit, QComboBox, QTimeEdit {
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 8px 12px;
        selection-background-color: #e3f2fd;
        background-color: white;
    }
    
    QLineEdit:focus, QComboBox:focus, QTimeEdit:focus {
        border: 1px solid #26A69A;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 20px;
    }
    
    QComboBox::down-arrow {
        width: 12px;
        height: 12px;
    }
    
    /* Прокрутка */
    QScrollBar:vertical {
        border: none;
        background: #f8f9fa;
        width: 8px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background: #adb5bd;
        min-height: 20px;
        border-radius: 4px;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    QScrollBar:horizontal {
        border: none;
        background: #f8f9fa;
        height: 8px;
        margin: 0px;
    }
    
    QScrollBar::handle:horizontal {
        background: #adb5bd;
        min-width: 20px;
        border-radius: 4px;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
    """