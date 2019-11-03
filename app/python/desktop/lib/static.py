from typing import Optional

from PyQt5.QtQml import QQmlApplicationEngine

qqmlApplicationEngine: Optional[QQmlApplicationEngine] = None


def init_qml_engine():
    global qqmlApplicationEngine
    qqmlApplicationEngine = QQmlApplicationEngine()


def get_qml_engine():
    global qqmlApplicationEngine
    return qqmlApplicationEngine
