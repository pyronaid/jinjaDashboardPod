import apps.auth_module.objects.UserDto as UserDto


class SignupRequestDto:
    def __init__(self, usernameProvided, passwordProvided, mailProvided):
        self.usernameProvided: str = usernameProvided
        self.passwordProvided: str = passwordProvided
        self.mailProvided: str = mailProvided


class SignupResponseDto:
    errorMsgUsername: str
    errorMsgPassword: str
    errorMsgMail: str
    responseCode: int
    responseMsg: str
    userObj: UserDto
