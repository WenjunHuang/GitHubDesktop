import asyncio
import os
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from asyncqt import QEventLoop

from desktop.lib.app_store import init_app_store
from desktop.lib.http import init_session
from desktop.lib.viewmodels.sign_in import SignInViewModel

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
loop = QEventLoop(app)
asyncio.set_event_loop(loop)
asyncio.events._set_running_loop(loop)
init_session()

def register_types():
    qmlRegisterType(SignInViewModel, "Desktop", 1, 0, SignInViewModel.__name__)


register_types()

config_dir = os.path.abspath(os.path.join(os.getcwd(), "../config"))
print(config_dir)
init_app_store(config_dir)

print(engine.importPathList())

engine.load("./test_sigin.qml")
if not engine.rootObjects():
    sys.exit(-1)

with loop:
    sys.exit(loop.run_forever())
