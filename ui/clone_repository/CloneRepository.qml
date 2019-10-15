import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import "../dialog"
import "../common" as C
import "../styles/variables.mjs" as Vars

GithubDialog {
    id: _dialog
    title: 'Clone a Repository'
    showFooter: false

    contentComponent: Component {
        C.Pane {
            ColumnLayout {
                width: parent.width
                C.TabBar {
                    id: _tabBar
                    Layout.fillWidth: true
                    C.TabButton {
                        text: 'GitHub.com'
                    }
                    C.TabButton {
                        text: 'GitHub Enterprise Server'
                    }
                    C.TabButton {
                        text: 'URL'
                    }
                }
                StackLayout {
                    id: stack
                    Layout.fillWidth: true
                    currentIndex: _tabBar.currentIndex
                    C.Pane {
                        id: _githubDotCom
                        property bool active: stack.currentIndex === 0

                        Binding {
                            target: _dialog
                            property: 'showFooter'
                            value: false
                            when: active
                        }

                        padding: Vars.spacing
                        width: parent.width

                        RowLayout {
                            width: parent.width
                            spacing: Vars.spacingX2
                            Text {
                                elide: Text.ElideRight
                                text: 'Sign in to your GitHub.com account to access your repositories.'
                                wrapMode: Text.WordWrap
                            }
                            C.PrimaryButton {
                                Layout.alignment: Qt.AlignBottom | Qt.AlignRight
                                implicitWidth: 120
                                text: 'Sign In'
                            }
                        }
                    }
                    C.Pane {
                        id: _githubEnterprise
                        property bool active: stack.currentIndex === 1

                        Binding {
                            target: _dialog
                            property: 'showFooter'
                            value: false
                            when: active
                        }

                        padding: Vars.spacing
                        width: parent.width

                        RowLayout {
                            width: parent.width
                            spacing: Vars.spacingX2
                            Text {
                                elide: Text.ElideRight
                                text: 'If you have a GitHub Enterprise Server account at work,sign in to it to get access to your repositories.'
                                wrapMode: Text.WordWrap
                            }
                            C.PrimaryButton {
                                Layout.alignment: Qt.AlignBottom | Qt.AlignRight
                                implicitWidth: 120
                                text: 'Sign In'
                            }
                        }
                    }

                    C.Pane {
                        id: _generic
                        property bool active: stack.currentIndex === 2

                        Binding {
                            target: _dialog
                            property: 'showFooter'
                            value: true
                            when: _generic.active
                        }

                        Binding {
                            target: _dialog
                            property: 'enableSubmit'
                            value: _urlOrUserName.text && _localPath.text
                            when: active
                        }

                        Binding {
                            target: _dialog
                            property: 'submitButtonText'
                            value: 'Clone'
                            when: active
                        }
                        Binding {
                            target: _dialog
                            property: 'dismissButtonText'
                            value: 'Cancel'
                            when: active
                        }

                        Connections {
                            target: _dialog
                            onSubmitted: {
                                console.log('ok')
                            }
                            enabled: active
                        }

                        padding: Vars.spacingX2
                        ColumnLayout {
                            width: parent.width
                            spacing: Vars.spacing
                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: Vars.spacing_third
                                Text {
                                    text: 'Repository URL or GitHub username and repository'
                                    font.pixelSize: Vars.font_size
                                }
                                Text {
                                    text: '(hubot/cool-repo)'
                                    font.pixelSize: Vars.font_size
                                }
                                C.TextInput {
                                    id: _urlOrUserName
                                    Layout.fillWidth: true
                                    placeholderText: 'URL or username/repository'
                                }
                            }
                            ColumnLayout {
                                Layout.fillWidth: true
                                RowLayout {
                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: Vars.spacing_third
                                        Text {
                                            text: 'Local Path'
                                            font.pixelSize: Vars.font_size
                                        }
                                        C.TextInput {
                                            Layout.fillWidth: true
                                            id: _localPath
                                        }
                                    }
                                    C.SecondaryButton {
                                        Layout.alignment: Qt.AlignBottom | Qt.AlignRight
                                        text: "Choose..."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
