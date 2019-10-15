import QtQuick 2.12
import QtQuick.Controls 2.12
import QtGraphicalEffects 1.0

Image{
    id: root
    property string symbol
    property alias color: overlay.color
    property bool showColor: false

    source: './' + symbol + '.svg'
    ColorOverlay {
        id:overlay
        visible: showColor
        anchors.fill: root
        source: root
    }
}
