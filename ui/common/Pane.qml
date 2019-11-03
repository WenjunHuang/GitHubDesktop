import QtQuick 2.12
import QtQuick.Templates 2.12 as T

T.Pane {
        id: control
    padding: 0
    leftInset: 0
    topInset: 0
    rightInset: 0
    bottomInset: 0


        implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                                contentWidth + leftPadding + rightPadding)
        implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                                 contentHeight + topPadding + bottomPadding)


        background: Rectangle {
            color: control.palette.window
        }
}
