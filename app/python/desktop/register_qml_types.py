from PyQt5.QtQml import qmlRegisterType

from desktop.lib.viewmodels.changes.changes_view_model import ChangesViewModel
from desktop.lib.viewmodels.sign_in import SignInViewModel

def register_qml_types():
    qmlRegisterType(SignInViewModel, "GitHubDesktop", 1, 0, SignInViewModel.__name__)
    qmlRegisterType(ChangesViewModel, "GitHubDesktop", 1, 0, ChangesViewModel.__name__)

