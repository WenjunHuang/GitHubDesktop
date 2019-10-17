import sys
import asyncio
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import qmlRegisterType
from asyncqt import QEventLoop

from desktop.lib.bloc import BlocBuilder
from desktop.lib.blocs.account_repositories.bloc import AccountRepositoriesBloc
from desktop.lib.http import init_session
from desktop.lib.static import qqmlApplicationEngine, init_qml_engine, get_qml_engine

app = QGuiApplication(sys.argv)
loop = QEventLoop(app)
asyncio.set_event_loop(loop)
asyncio.events._set_running_loop(loop)

# loop = asyncio.get_event_loop()
token = 'c415e9d535a95a28ecf955c01487330ebfa646e7'
endpoint = "https://api.github.com"
# self.api_repositories_store = ApiRepositoriesStore(FakeAccountStore())
init_session()
init_qml_engine()
engine = get_qml_engine()
qmlRegisterType(BlocBuilder, 'Desktop', 1, 0, 'BlocBuilder')

repo_bloc = AccountRepositoriesBloc()
engine.rootContext().setContextProperty('AccountRepositoryBloc', repo_bloc)
engine.load(QUrl("test_account_repositories.qml"))
if not engine.rootObjects():
    sys.exit(-1)

with loop:
    sys.exit(loop.run_forever())
