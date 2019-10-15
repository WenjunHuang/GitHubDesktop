import QtQuick 2.12
import QtQuick.Controls 2.12
import "./styles/variables.mjs" as Vars
import './styles/color_system.mjs' as Colors

Item {
    width: 640
    height: 480

    Rectangle {
        id: root
        anchors.fill: parent
        gradient: Vars.skeleton_background_gradient(root,Colors.red)
//        gradient:Gradient{
//            orientation:Gradient.Horizontal
//            GradientStop{position:0.0;color:Qt.rgba(1,1,1,0)}
//            GradientStop{position:0.5;color:Qt.rgba(1,1,1,0.5)}
//            GradientStop{position:1.0;color:Qt.rgba(1,1,1,0)}
//        }
        //color:Colors.hexPlusAlpha(Colors.red,0.5)

        Component.onCompleted: {
            //console.log(Vars.text_color)
        }
        border {
            style
        }
    }
}
