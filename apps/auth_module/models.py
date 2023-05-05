# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import base64

# Flask modules
from apps import login_manager
from flask_login import UserMixin
from flask import redirect, request

class User (UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    return User.get(user_id)


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
