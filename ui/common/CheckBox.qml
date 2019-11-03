import QtQuick 2.12
import QtQuick.Templates 2.12 as T
import QtGraphicalEffects 1.13
import "../styles/variables.mjs" as Vars
import "../styles/color_system.mjs" as Colors
import "../octicons"

T.CheckBox {
    id: control
    padding: 0

    indicator: Rectangle {
        implicitWidth: 12
        implicitHeight: 12
        x: control.leftPadding
        y: parent.height / 2 - height / 2
        radius: 3
        border.color: Vars.box_border_color

        Rectangle {
            anchors.fill: parent
            radius: 3
            color: Vars.button_background
            visible: control.checked
            Octicon {
                id: _checkIcon
                anchors.centerIn: parent
                symbol: 'check'
                width: 10
                height: 12
            }

            ColorOverlay {
                anchors.fill: _checkIcon
                source: _checkIcon
                color: Colors.white
            }
        }
    }

    contentItem: Text {
        text: control.text
        font: control.font
        color: Vars.text_color
        verticalAlignment: Text.AlignVCenter
        leftPadding: control.indicator.width + control.spacing
    }
}
