from PySide2.QtWidgets import QMessageBox


def msg_info(message):
    QMessageBox(QMessageBox.Information, '信息', message).exec_()


def msg_warn(message):
    QMessageBox(QMessageBox.Warning, '警告', message).exec_()


def msg_error(message):
    QMessageBox(QMessageBox.Critical, '错误', message).exec_()
