# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64
from datetime import datetime
import re
# Flask modules
from apps import login_manager
from flask_login import UserMixin
from flask import redirect, request, session
from apps.auth_module.objects.LoginDto import LoginResponseDto, LoginRequestDto
from apps.auth_module.objects.SignupDto import SignupResponseDto, SignupRequestDto


class User(UserMixin):
    id: str
    username: str
    email: str
    firstSubscriptionDate: datetime

    def get_id(self) -> str:
        return self.id


@login_manager.user_loader
def user_loader(user_id):
    return session.get(user_id, None)


@login_manager.request_loader
def request_loader(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/authentication/login?next=' + request.path)


def convertResponseToUser(loginResponseDto: LoginResponseDto) -> User:
    userConverted = User()
    if loginResponseDto.userObj is not None:
        userConverted.email = loginResponseDto.userObj.email
        userConverted.username = loginResponseDto.userObj.username
        userConverted.firstSubscriptionDate = loginResponseDto.userObj.firstSubscriptionDate
        return userConverted
    else:
        return None


def convertResponseToUser(signupResponseDto: SignupResponseDto) -> User:
    userConverted = User()
    regex = re.compile(r"(\.\d{6})\d{0,1}$", re.IGNORECASE)
    if signupResponseDto.userObj is not None:
        userConverted.id = signupResponseDto.userObj.id
        userConverted.email = signupResponseDto.userObj.email
        userConverted.username = signupResponseDto.userObj.username
        userConverted.firstSubscriptionDate = datetime.strptime(re.sub(regex, '\\1', signupResponseDto.userObj.firstSubscriptionDate), "%Y-%m-%dT%H:%M:%S.%f")
        return userConverted
    else:
        return None
