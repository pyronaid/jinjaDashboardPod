import apps.auth_module.objects.UserDto as UserDto


class LoginRequestDto:
    def __init__(self, usernameProvided, passwordProvided):
        self.usernameProvided: str = usernameProvided
        self.passwordProvided: str = passwordProvided


class LoginResponseDto:
    errorMsgUsername: str
    errorMsgPassword: str
    responseCode: int
    responseMsg: str
    userObj: UserDto
