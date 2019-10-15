import QtQuick 2.12
import QtQuick.Controls 2.12
import "../common" as C
import "../styles/variables.mjs" as Vars

Rectangle {
    property alias text: badgeText.text
    id: root

    implicitHeight: badgeText.implicitHeight + 2 * 2
    implicitWidth: badgeText.implicitWidth + 2 * 5
    radius: height / 2

    color: Vars.tab_bar_count_background_color
    Text {
        id: badgeText
        font.pixelSize: Vars.font_size_xs
        font.weight: Font.Bold
        text:"5"
        anchors.centerIn: parent
    }
}
