import apps.auth_module.objects.UserDto as UserDto


class SignupRequestDto:
    def __init__(self, usernameProvided, passwordProvided, mailProvided):
        self.usernameProvided: str = usernameProvided
        self.passwordProvided: str = passwordProvided
        self.mailProvided: str = mailProvided


class SignupResponseDto:
    def __init__(self):
        self.errorMsgUsername: str = None
        self.errorMsgPassword: str = None
        self.errorMsgMail: str = None
        self.responseCode: int = None
        self.responseMsg: str = None
        self.userObj: UserDto = None
