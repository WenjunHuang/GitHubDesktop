import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.2
import "../common" as C
import "../dialog"
import "../styles/variables.mjs" as Vars

GithubDialog {
    title: 'Add Local Repository'
    submitButtonText: 'Add Repository'
    dismissButtonText: 'Cancel'

    contentComponent: Component {
        C.Pane {
            RowLayout {
                anchors.left: parent.left
                anchors.right: parent.right
                spacing: Vars.spacing
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Vars.spacing_third
                    Text {
                        Layout.fillWidth: true
                        text: 'Local Path'
                        font.pixelSize: Vars.font_size
                    }

                    C.TextInput {
                        Layout.fillWidth: true
                        id: _repositoryPath
                        placeholderText: 'repository path'
                    }
                }
                C.SecondaryButton {
                    id: _chooseButton
                    Layout.alignment: Qt.AlignBottom
                    text: 'Choose...'
                    onClicked: {
                        fileDialog.open()
                    }
                }
            }
        }
    }

    FileDialog {
        id: fileDialog
        modality: Qt.WindowModal
        title: "Choose a folder"
        selectFolder: true
        selectedNameFilter: "All files (*)"
        onAccepted: {
            console.log("Accepted: " + fileUrls)
        }
        onRejected: {
            console.log("Rejected")
        }
    }
}
