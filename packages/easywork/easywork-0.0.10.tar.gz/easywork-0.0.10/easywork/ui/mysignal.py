from PySide2.QtCore import *
from PySide2.QtWidgets import *


class MySignal(QObject):
    log_debug = Signal(str)
    log_info = Signal(str)
    log_warning = Signal(str)
    log_error = Signal(str)
    log_critical = Signal(str)
    table_refresh = Signal(QTableWidget, list)
    table_insert = Signal(QTableWidget, list)
    table_update = Signal(QTableWidget, int, list)
    table_item = Signal(QTableWidget, int, int, str)
    table_clear = Signal(QTableWidget)

    def __init__(self, log_widget, log_factory):
        super().__init__()
        self.log_widget = log_widget
        self.log_factory = log_factory
        self.log_debug.connect(self.log_debug_handle)
        self.log_info.connect(self.log_info_handle)
        self.log_warning.connect(self.log_warning_handle)
        self.log_error.connect(self.log_error_handle)
        self.log_critical.connect(self.log_critical_handle)
        self.table_refresh.connect(self.table_refresh_handle)
        self.table_insert.connect(self.table_insert_handle)
        self.table_update.connect(self.table_update_handle)
        self.table_item.connect(self.table_item_handle)
        self.table_clear.connect(self.table_clear_handle)

    def log_debug_handle(self, text):
        self.log_widget.append(f'<font color="#548c26">{text}</font>')
        self.log_factory.debug(text)

    def log_info_handle(self, text):
        self.log_widget.append(f'<font color="#548c26">{text}</font>')
        self.log_factory.info(text)

    def log_warning_handle(self, text):
        self.log_widget.append(f'<font color="#a89022">{text}</font>')
        self.log_factory.warning(text)

    def log_error_handle(self, text):
        self.log_widget.append(f'<font color="#db5451">{text}</font>')
        self.log_factory.error(text)

    def log_critical_handle(self, text):
        self.log_widget.append(f'<font color="#a575ba">{text}</font>')
        self.log_factory.critical(text)

    def table_refresh_handle(self, table, contents_list):
        self.table_clear_handle(table)
        for contents in contents_list:
            self.table_insert_handle(table, contents)

    def table_insert_handle(self, table, contents):
        row = table.rowCount()
        table.setRowCount(row + 1)
        for column, content in enumerate(contents):
            self.table_item_handle(table, row, column, content)

    def table_update_handle(self, table, row, contents):
        for column, content in enumerate(contents):
            self.table_item_handle(table, row, column, content)

    def table_item_handle(self, table, row, column, content):
        item = QTableWidgetItem(str(content))
        item.setFlags(Qt.ItemIsEnabled)
        table.setItem(row, column, item)

    def table_clear_handle(self, table):
        table.setRowCount(0)
