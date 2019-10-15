import QtQuick 2.12
import '../styles/variables.mjs' as Vars

Button {
    id: control
    implicitHeight: Vars.button_height
    hoverEnabled: true
    opacity: enabled ? 1.0 : 0.6
    contentItem: Text {
        text: control.text
        font {
            pixelSize: Vars.font_size
        }
        color: Vars.button_text_color
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    background: Rectangle {
        radius: Vars.border_radius
        border.width: Vars.base_border_width
        border.color: Vars.base_border_color
        color: (hovered
                && enabled) ? Vars.button_hover_background : Vars.button_background
    }
}
