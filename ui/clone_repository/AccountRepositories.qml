import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import Desktop 1.0
import "../dialog"
import "../common" as C
import "../octicons"
import "../styles/variables.mjs" as Vars

C.Pane {
    property string endpoint
    property string token

    id: root
    padding: Vars.spacingX2


    function splitUserFromOrg(repositories){

        const user = []
        const org = []
        for (var repos of repositories){
            if (repos.owner.type === 'User')
                user.push(repos)
            else
                org.push(repos)
        }

        return [user,org]
    }

    function fillListView(repositories){
        repositoryModel.clear()

        const filterText = filter.text
        if (filterText) {
            repositories = repositories.filter(repos=>repos.name.includes(filterText))
        }

        // split user repositories from organization repositories
        const [user, org] = splitUserFromOrg(repositories)
        repositoryModel.append({group:true,name:'Your Repositories'})
        for (var repos of user)
            repositoryModel.append(repos)

        repositoryModel.append({group:true,name:'Organizations'})
        for (var repos of org)
            repositoryModel.append(repos)

        root.state = 'success'
        repositoryView.currentIndex = -1
    }

    BlocBuilder {
        id: bloc
        blocName: 'AccountRepositoryBloc'

        onStateChanged: {
            var name = state.name
            console.log(name)
            if (name === 'RepositoryNotLoadedState') {
                bloc.dispatch('LoadAccountRepositoryEvent',{endpoint:endpoint,token:token})
                root.state = 'uninited'
            } else if (name === 'LoadingAccountRepositoriesState') {
                root.state = 'loading'
            } else if (name === 'AccountRepositoriesLoadedState') {
                root.fillListView(state.repositories)
            } else if (name === 'FailToLoadAccountRepositoriesState') {
                root.state = 'failed'
            }
        }

    }

    ColumnLayout {
        width: parent.width
        height: parent.height
        spacing: Vars.spacing
        RowLayout {
            Layout.fillWidth: true
            spacing: Vars.spacing

            C.TextInput {
                id: filter
                Layout.fillWidth: true
                placeholderText: 'Filter'
                onTextModified: {
                    const state = bloc.currentState()
                    if (state && state.name === 'AccountRepositoriesLoadedState') {
                        root.fillListView(state.repositories)
                    }
                }
            }
            C.SecondaryButton {
                id: refreshButton
                enabled: root.state != 'loading'
                Layout.alignment: Qt.AlignRight
                image: Octicon {
                    id: icon
                    symbol: 'sync'
                    width: 12
                    height: 16
                }

                RotationAnimation {
                    id: refreshAnimation
                    loops: Animation.Infinite
                    target: icon
                    from: 0
                    to: 360
                    duration: 2000
                    running: false
                }

                onClicked: {
                    bloc.dispatch('LoadAccountRepositoryEvent',{endpoint:endpoint,token:token})
                }
            }
        }

        ListModel {
            id: repositoryModel
        }

        ListView {
            id: repositoryView
            model: repositoryModel
            Layout.fillWidth: true
            Layout.fillHeight: true
            delegate: repositoryComponent
            highlight: Rectangle {
                color: Vars.button_background
            }
            highlightMoveDuration: 0
            clip: true
            ScrollBar.vertical: ScrollBar {
            }
        }

        C.PrimaryButton {
            Layout.fillWidth: true
            enabled: repositoryView.currentIndex != -1
            visible: repositoryView.currentIndex != -1
            text: repositoryView.currentIndex !== -1?'Clone ' + '<b>'+repositoryModel.get(repositoryView.currentIndex).name +'</b>':""
        }
    }

    Component {
        id: repositoryComponent
        C.Pane {
            leftPadding: Vars.spacing
            rightPadding: Vars.spacing
            topPadding: Vars.spacing_half
            bottomPadding: Vars.spacing_half
            width: parent.width
            contentHeight: repositoryName.implicitHeight
            background: Rectangle {
                color:(hovered && repositoryView.currentIndex != index )?Vars.secondary_button_background:'transparent'
            }

            hoverEnabled: true

            RowLayout {
                id: item
                spacing: Vars.spacing_half
                Octicon {
                    visible: !model.group
                    symbol: getIcon(model['private'], fork)
                    width:12
                    height:16
                    color: repositoryView.currentIndex == index ? Vars.box_selected_active_text_color:Vars.text_color
                    showColor: true
                    function getIcon(isPrivate,isFork) {
                        if (isPrivate) {
                            return "lock"
                        }
                        if (isFork) {
                            return "repo-forked"
                        }

                        return "repo"
                    }
                }

                Text {
                    id: repositoryName
                    text: model.group?model.name:model.owner.login + '/' + model.name
                    font.pixelSize: Vars.font_size
                    font.bold: model.group?true:false
                    color: repositoryView.currentIndex == index ? Vars.box_selected_active_text_color:Vars.text_color
                }
            }

            MouseArea {
                anchors.fill: parent
                enabled: !model.group
                onClicked: {
                    repositoryView.currentIndex = index
                }
            }
        }
    }
    states: [
        State {
            name: 'uninit'
        },
        State {
            name: 'loading'
            StateChangeScript {
                script: {
                    refreshButton.enabled = false
                    refreshAnimation.start()
                }
            }
        },
        State {
            name: 'success'
            StateChangeScript {
                script: {
                    refreshAnimation.stop()
                    refreshButton.enabled = true
                }
            }
        },
        State {
            name: 'failed'
            StateChangeScript {
                script: {
                    refreshAnimation.stop()
                }
            }
        }
    ]
}
