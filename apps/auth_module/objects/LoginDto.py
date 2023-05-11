import apps.auth_module.objects.UserDto as UserDto


class LoginRequestDto:
    def __init__(self, usernameProvided, passwordProvided):
        self.usernameProvided: str = usernameProvided
        self.passwordProvided: str = passwordProvided


class LoginResponseDto:
    def __init__(self):
        self.errorMsgUsername: str = None
        self.errorMsgPassword: str = None
        self.responseCode: int = None
        self.responseMsg: str = None
        self.userObj: UserDto = None
