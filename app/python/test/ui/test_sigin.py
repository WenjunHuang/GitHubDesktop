import asyncio
import os
import sys

from PyQt5.QtQml import QQmlApplicationEngine

from desktop.run_app import run_app


class TestBootstrap:
    def __init__(self, qml_engine: QQmlApplicationEngine, event_loop):
        self.qml_engine = qml_engine
        self.event_loop = event_loop

    def run(self):
        self.qml_engine.load(os.path.join(os.getcwd(), "app/python/test/ui/test_signin.qml"))
        with self.event_loop:
            sys.exit(self.event_loop.run_forever())


config_dir = os.path.abspath(os.path.join(os.getcwd(), "app/python/test/config"))

run_app(TestBootstrap, config_dir)
