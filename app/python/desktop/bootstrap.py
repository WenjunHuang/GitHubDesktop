import sys

from PyQt5.QtQml import QQmlApplicationEngine


class Bootstrap:
    def __init__(self, qml_engine: QQmlApplicationEngine, event_loop):
        self.qml_engine = qml_engine
        self.event_loop = event_loop

    def run(self):
        self.qml_engine.load("./ui/main.qml")
        with self.event_loop:
            sys.exit(self.event_loop.run_forever())
