import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.13
import "../common" as C
import "../octicons"
import "../styles/variables.mjs" as Vars

C.Pane {
    id: _dialog
    property string title

    property bool showFooter:true
    property string submitButtonText
    property string dismissButtonText

    property alias enableSubmit: _submitButton.enabled
    property bool loading: false
    property bool dismissable: true

    property alias dialogContent: _contentLoader.item

    property bool showError: false
    property string errorText

    property Component contentComponent

    signal dismissed
    signal submitted

    padding: 0
    implicitWidth: 400

    ColumnLayout {
        anchors.left: parent.left
        anchors.right: parent.right
        spacing: 0
        C.Pane {
            Layout.fillWidth: true
            //contentHeight: _title.implicitHeight
            //contentHeight: 50
            implicitHeight: 50
            padding: Vars.spacingX2

            Text {
                id: _title
                text: title
                font {
                    weight: Vars.font_weight_semibold
                    pixelSize: Vars.font_size_md
                }
                color: Vars.text_color
                anchors.left: parent.left
            }

            Octicon {
                id: _loadingIcon
                symbol: 'sync'
                width: 12
                height: 16
                anchors.left: _title.right
                anchors.leftMargin: Vars.spacing
                anchors.verticalCenter: parent.verticalCenter
            }

            Octicon {
                id: _closeIcon
                symbol: 'x'
                width: 12
                height: 16
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                visible: dismissable
                MouseArea {
                    anchors.fill: parent
                    onClicked: dismissed()
                }
            }

            ColorOverlay {
                anchors.fill: _closeIcon
                source: _closeIcon
                color: Vars.text_secondary_color
                visible: dismissable
            }

            RotationAnimation {
                id: _loadingIconAnimation
                target: _loadingIcon
                direction: RotationAnimation.Clockwise
                loops: Animation.Infinite
                from: 0
                to: 360
                duration: 1000
                running: false
            }

            states: [
                State {
                    name: "normal"
                    when: !loading
                    StateChangeScript {
                        script: _loadingIconAnimation.stop()
                    }
                    PropertyChanges {
                        target: _loadingIcon
                        visible: false
                    }
                },
                State {
                    name: "loading"
                    when: loading
                    PropertyChanges {
                        target: _loadingIcon
                        visible: true
                    }
                    StateChangeScript {
                        script: _loadingIconAnimation.start()
                    }
                }
            ]
        }

        Rectangle {
            height: 1
            id: _headerDivider
            color: Vars.box_border_color
            Layout.fillWidth: true
            z: 1
        }

        C.Pane {
            id: _error
            Layout.fillWidth: true
            padding: Vars.spacing
            visible: showError
            contentHeight: _text.implicitHeight

            Octicon {
                id: _icon
                symbol: 'stop'
                width: 14
                height: 16
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            }

            ColorOverlay {
                anchors.fill: _icon
                source: _icon
                color: Vars.form_error_text_color
                visible: dismissable
            }

            Text {
                id: _text
                text: errorText
                anchors.left: _icon.right
                anchors.leftMargin: Vars.spacing
                font.pixelSize: Vars.font_size
                color: Vars.form_error_text_color
            }

            background: Rectangle {
                color: Vars.form_error_background
            }
        }

        Rectangle {
            id: _errorDivider
            height: 1
            color: Vars.form_error_border_color
            visible: showError ? true : false
            Layout.fillWidth: true
        }

        C.Pane {
            id: _content
            Layout.fillWidth: true

            Loader {
                id: _contentLoader
                anchors.left: parent.left
                anchors.right: parent.right
                sourceComponent: contentComponent
            }
        }

        Rectangle {
            id: _contentDivider
            height: 1
            color: Vars.box_border_color
            Layout.fillWidth: true
            visible: showFooter
        }

        C.Pane {
            id: _footer
            padding: Vars.spacingX2
            contentHeight: _cancelButton.implicitHeight
            Layout.fillWidth: true
            visible:showFooter

            C.SecondaryButton {
                id: _cancelButton
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                implicitWidth: 120
                text: dismissButtonText
                onClicked: dismissed()
            }
            C.PrimaryButton {
                id: _submitButton
                text: submitButtonText
                implicitWidth: 120
                anchors.right: _cancelButton.left
                anchors.rightMargin: Vars.spacing_half
                anchors.verticalCenter: parent.verticalCenter
                onClicked: submitted()
            }
        }
    }
}
