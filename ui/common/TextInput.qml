import QtQuick 2.12
import QtQuick.Controls 2.12
import "../styles/variables.mjs" as Vars
import "../octicons"

Rectangle {
    id: control
    property alias text: _textInput.text
    property alias echoMode: _textInput.echoMode
    property int millisBeforeTriggerTextChanged: 200
    property string placeholderText

    signal textModified

    border.width: 1
    border.color: _textInput.focus ? Vars.focus_color : Vars.box_border_color
    radius: Vars.border_radius
    implicitHeight: _textInput.implicitHeight

    TextInput {
        id: _textInput
        anchors.fill: parent
        leftPadding: Vars.spacing_half
        rightPadding: Vars.spacing_half
        topPadding: Vars.spacing_third
        bottomPadding: Vars.spacing_third
        font.pixelSize: Vars.font_size

        onTextChanged: {
            timer.restart()
        }
    }

    Text {
        text: placeholderText
        anchors.fill: parent
        color: Vars.box_border_color
        leftPadding: Vars.spacing_half
        rightPadding: Vars.spacing_half
        topPadding: Vars.spacing_third
        bottomPadding: Vars.spacing_third
        visible: placeholderText && !_textInput.text && !_textInput.focus
    }

    Octicon {
        symbol: 'x'
        width: 12
        height: 16
        visible: _textInput.text && _textInput.focus ? true : false
        color: Vars.focus_color
        showColor: true

        anchors.right: _textInput.right
        anchors.rightMargin: Vars.spacing_half
        anchors.verticalCenter: _textInput.verticalCenter

        MouseArea {
            anchors.fill: parent
            onClicked: {
                _textInput.text = ''
                _textInput.textChanged()
            }
        }
    }

    Timer {
        id: timer
        repeat: false
        running: false
        interval: control.millisBeforeTriggerTextChanged
        onTriggered: control.textModified()
    }
}
