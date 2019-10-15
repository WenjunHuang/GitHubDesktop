import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import "../common" as C
import "../dialog"
import "../octicons"
import "../styles/variables.mjs" as Vars

GithubDialog {
    id: _dialog
    title: 'Sign in'
    submitButtonText: 'Sign in'
    dismissButtonText: 'Cancel'
    enableSubmit: dialogContent.userAccount.text
                  && dialogContent.userPassword.text

    contentComponent: Component {
        C.Pane {
            property alias userAccount: _userAccount.text
            property alias userPassword: _userPassword.text
            padding: Vars.spacingX2
            ColumnLayout {
                spacing: Vars.spacing
                anchors.left: parent.left
                anchors.right: parent.right

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Vars.spacing_third
                    Text {
                        Layout.fillWidth: true
                        text: 'User name or email addres'
                        font.pixelSize: Vars.font_size
                    }
                    C.TextInput {
                        id: _userAccount
                        Layout.fillWidth: true
                    }
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Vars.spacing_third
                    Text {
                        Layout.fillWidth: true
                        text: 'password'
                        font.pixelSize: Vars.font_size
                    }
                    C.TextInput {
                        id: _userPassword
                        Layout.fillWidth: true
                        echoMode: TextInput.Password
                    }
                }

                Text {
                    id: _forgotPassword
                    Layout.fillWidth: true
                    text: 'Forgot password?'
                    color: Vars.link_button_color
                    font.pixelSize: Vars.font_size
                    font.underline: _forgotPasswordMA.containsMouse
                    horizontalAlignment: Text.AlignRight
                    MouseArea {
                        id: _forgotPasswordMA
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: Vars.spacing_half
                    Pane {
                        Layout.fillWidth: true
                        contentHeight: _or.implicitHeight
                        padding: 0
                        Rectangle {
                            height: 1
                            color: Vars.box_border_color
                            Layout.fillWidth: true
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        C.Pane {
                            anchors.centerIn: parent
                            anchors.verticalCenterOffset: -3
                            Text {
                                id: _or
                                text: "or"
                                font.pixelSize: Vars.font_size
                            }
                        }
                    }
                    C.Pane {
                        Layout.fillWidth: true
                        contentHeight: _externalText.implicitHeight
                        RowLayout {
                            anchors.centerIn: parent
                            Text {
                                id: _externalText
                                Layout.fillWidth: true
                                text: 'Sign in using your browser'
                                color: Vars.link_button_color
                                font.pixelSize: Vars.font_size
                                font.underline: _externalTextMA.containsMouse
                                MouseArea {
                                    id: _externalTextMA
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                                }
                            }
                            Octicon {
                                id: _loadingIcon
                                symbol: 'link-external'
                                width: 12
                                height: 16
                            }
                        }
                    }
                }
            }
        }
    }

    onSubmitted: {
        loading = true
        showError = true
        errorText = 'Error'
    }

    onDismissed: {
        console.log("dismissed press")
    }
}
