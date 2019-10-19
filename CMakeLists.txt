cmake_minimum_required(VERSION 3.1)

project(desktop LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 COMPONENTS Core Quick REQUIRED)


add_executable(${PROJECT_NAME} "./ui/main.qml"
    "./ui/styles/color_system.mjs"
    "./ui/styles/variables.mjs"
    "./ui/signin/SigninDialog.qml"
    "./ui/common/Border.qml"
    "./ui/common/Pane.qml"
    "./ui/common/TextInput.qml"
    "./ui/common/CheckBox.qml"
    "./ui/common/ComboBox.qml"
    "./ui/common/TabButton.qml"
    "./ui/common/TabBar.qml"
    "./ui/common/PrimaryButton.qml"
    "./ui/common/SecondaryButton.qml"
    "./ui/common/Button.qml"
    "./ui/dialog/GithubDialog.qml"
    "./ui/octicons/Octicon.qml"
    "./ui/add_repository/AddExistingRepository.qml"
    "./ui/add_repository/CreateRepository.qml"
    "./ui/clone_repository/AccountRepositories.qml"
    "./ui/clone_repository/CloneGithubRepository.qml"
    "./ui/clone_repository/CloneRepository.qml"
    "./ui/Repository.qml"
    "./ui/changes/FileChangedBadge.qml"
    "./ui/changes/ChangesSideBar.qml"
    )
target_compile_definitions(${PROJECT_NAME} PRIVATE $<$<OR:$<CONFIG:Debug>,$<CONFIG:RelWithDebInfo>>:QT_QML_DEBUG>)
target_link_libraries(${PROJECT_NAME} PRIVATE Qt5::Core Qt5::Quick)

