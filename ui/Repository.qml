import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import "./common" as C
import "./changes"
import "./styles/variables.mjs" as Vars

C.Pane {
    id: root
    ColumnLayout {
        width:parent.width
        C.TabBar {
            id: _tabBar
            Layout.fillWidth: true
            C.TabButton {
                text: 'Changes'
            }
            C.TabButton {
                text: 'History'
            }
        }
        StackLayout {
            id: stack
            Layout.fillWidth: true
            currentIndex: _tabBar.currentIndex
            C.Pane {
                id: changesPane
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
                id: historyPane
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

        }
    }

}

