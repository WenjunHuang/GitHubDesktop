from enum import IntEnum


class ComputedAction(IntEnum):
    # The action is being computed in the background
    Loading = 0
    # The action should complete without any additional work required by the user
    Clean = 1
    # the action requires additional work by the user to complete successfully
    Conflicts = 2
    # The action cannot be completed, for reasons the app should explain
    Invalid = 3
