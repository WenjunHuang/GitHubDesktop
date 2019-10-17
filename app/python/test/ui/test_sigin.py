import os
import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

from desktop.lib.app_store import init_app_store
from desktop.lib.viewmodels.sign_in import SignInViewModel

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()


def register_types():
    qmlRegisterType(SignInViewModel, "Desktop", 1, 0, SignInViewModel.__name__)


register_types()

config_dir = os.path.abspath(os.path.join(os.getcwd(), "../config"))
print(config_dir)
init_app_store(config_dir)

print(engine.importPathList())

engine.load("./test_sigin.qml")
sys.exit(app.exec_())
