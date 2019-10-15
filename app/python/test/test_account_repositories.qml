import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 2.0
import '../ui/clone_repository'


Window {
    id: root
    width: 640
    height: 480
    visible: true
    title:'Hello Python World!'

    AccountRepositories{
    //token : '95b3a27ff61fc3a09f3795ebf1d923282d7ad894'
    token:'1a97c7a098957d4056d76e9b848f15891d5c123e'
    endpoint : "https://api.github.com"
        anchors.fill: parent
    }

}