from PySide2.QtCore import *


class MySignal(QObject):
    log_debug = Signal(str)
    log_info = Signal(str)
    log_warning = Signal(str)
    log_error = Signal(str)
    log_critical = Signal(str)

    def __init__(self, log_widget, log_factory):
        super().__init__()
        self.log_widget = log_widget
        self.log_factory = log_factory
        self.log_debug.connect(self.log_debug_handle)
        self.log_info.connect(self.log_info_handle)
        self.log_warning.connect(self.log_warning_handle)
        self.log_error.connect(self.log_error_handle)
        self.log_critical.connect(self.log_critical_handle)

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
