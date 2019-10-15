import QtQuick 2.12
import QtQuick.Layouts 1.12
import "../styles/variables.mjs" as Vars

Button {
    id: control
    implicitHeight: Vars.button_height
    hoverEnabled: true
    opacity: enabled ? 1.0 : 0.6
    property Item image

    contentItem: RowLayout {
        spacing: Vars.spacing_half
        Item {
            Layout.alignment: Qt.AlignHCenter|Qt.AlignLeft
            visible: control.image ? true : false
            children: control.image ? [control.image] : []
            implicitHeight: control.image ? control.image.implicitHeight : 0
            implicitWidth: control.image ? control.image.implicitWidth : 0
        }

        Text {
            visible: control.text ? true : false
            text: control.text
            font {
                pixelSize: Vars.font_size
            }
            color: Vars.secondary_button_text_color
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    background: Rectangle {
        radius: Vars.border_radius
        border.width: Vars.base_border_width
        border.color: Vars.base_border_color
        color: Vars.secondary_button_background
    }
}
