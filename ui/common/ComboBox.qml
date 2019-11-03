import QtQuick 2.12
import QtQuick.Templates 2.12 as T
import "../styles/variables.mjs" as Vars
import "../styles/color_system.mjs" as Colors

T.ComboBox {
    id: control

    delegate: ItemDelegate {
        width: control.width
        contentItem: Text {
            text: modelData
            color: Vars.text_color
            font.pixelSize: Vars.font_size
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }
        highlighted: control.highlightedIndex === index
    }

    indicator: Canvas {
        id: canvas
        x: control.width - width - control.rightPadding
        y: control.topPadding + (control.availableHeight - height) / 2
        height: 12
        width: 6
        contextType: "2d"

        Connections {
            target: control
            onPressedChanged: canvas.requestPaint()
        }

        onPaint: {
            var gap = 2
            context.reset()
            context.moveTo(0, (height - gap) / 2)
            context.lineTo(width, (height - gap) / 2)
            context.lineTo(width / 2, 0)
            context.closePath()

            context.moveTo(0, (height + gap) / 2)
            context.lineTo(width, (height + gap) / 2)
            context.lineTo(width / 2, height)
            context.closePath()
            context.fillStyle = Colors.black
            context.fill()
        }
    }

    contentItem: Text {
        leftPadding: Vars.spacing
        rightPadding: control.indicator.width + Vars.spacing

        text: control.displayText
        font.pixelSize: Vars.font_size
        color: Vars.text_color
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        implicitWidth: 120
        implicitHeight: Vars.text_field_height
        border.color: control.focus ? Vars.focus_color : Vars.box_border_color
        border.width: control.visualFocus ? 2 : 1
        radius: Vars.border_radius
    }

    popup: Popup {
        y: control.height - 1
        width: control.width
        implicitHeight: contentItem.implicitHeight
        padding: 1

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex

            ScrollIndicator.vertical: ScrollIndicator {
            }
        }

        background: Rectangle {
            border.color: Vars.box_border_color
            radius: Vars.border_radius
        }
    }
}
