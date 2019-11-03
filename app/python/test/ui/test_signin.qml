import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12
import "../../../../ui/signin" as S

Window {
    width: 480
    height: 480
    visible: true
    S.SigninDialog {
        anchors.fill: parent
    }
}