from enum import Enum, unique, auto, IntEnum

kAuthenticatorAppWelcomeText = "Open the two-factor authentication app on your device to view your authentication " \
                               "code and verify your identity. "
kSmsMessageWelcomeText = "We just sent you a message via SMS with your authentication code. Enter the code in the " \
                         "form below to verify your identity. "


@unique
class AuthenticationMode(IntEnum):
    Sms = 0
    App = 1


def get_welcome_message(type: AuthenticationMode) -> str:
    if type == AuthenticationMode.Sms:
        return kSmsMessageWelcomeText
    elif type == AuthenticationMode.App:
        return kAuthenticatorAppWelcomeText
    else:
        return ""
