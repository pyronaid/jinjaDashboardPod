# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, request, redirect, flash, abort, url_for
from flask_login import login_user, login_required

from apps.auth_module import blueprint
from apps.auth_module.forms import LoginForm, CreateAccountForm
from apps.auth_module.util import verify_user, my_url_has_allowed_host_and_scheme, hash_pass
import apps.auth_module.be_calls as be_calls
from apps.auth_module.models import User, convertResponseToUser
from apps.auth_module.objects.LoginDto import LoginResponseDto, LoginRequestDto


@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/accounts/auth-signin/')
def accounts_signin():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    login_form = LoginForm(request.form)
    error_username: str = None
    error_password: str = None
    if login_form.validate_on_submit():
        # read form data
        username = request.form['username']
        password = request.form['password']
        # Locate user
        loginResponseDto: LoginResponseDto = be_calls.process_login(username, hash_pass(password))
        if loginResponseDto is not None:
            error_username = loginResponseDto.errorMsgUsername
            error_password = loginResponseDto.errorMsgPassword
        user: User = convertResponseToUser(loginResponseDto)
        if user and verify_user(password):
            # Login and validate the user.
            # user should be an instance of your `User` class
            login_user(user)
            flash('Logged in successfully.')
            # url_has_allowed_host_and_scheme should check if the url is safe
            # for redirects, meaning it matches the request host.
            # See Django's url_has_allowed_host_and_scheme for an example.
            next = request.args.get('next')
            if not my_url_has_allowed_host_and_scheme(next, request.host):
                return abort(400)
            redirect(next or url_for('dashboard_blueprint.index'))
    return render_template('accounts/auth-signin.html', segment='signin', parent='accounts', form=login_form, error_username=error_username, error_password=error_password)


@blueprint.route('/register', methods=['GET', 'POST'])
@blueprint.route('/accounts/auth-signup/')
def accounts_signup():
    create_account_form = CreateAccountForm(request.form)
    return render_template('accounts/auth-signup.html', segment='signup', parent='accounts', form=create_account_form)


# Accounts
@blueprint.route('/accounts/forgot-password/')
def accounts_forgot_password():
    return render_template('accounts/forgot-password.html', segment='forgot-password', parent='accounts')

@blueprint.route('/accounts/password-change/')
@login_required
def accounts_password_change():
    return render_template('accounts/password_change.html', segment='password-change-done', parent='accounts')

@blueprint.route('/accounts/password-change-done/')
@login_required
def accounts_password_change_done():
    return render_template('accounts/password_change_done.html', segment='password-change-done', parent='accounts')

@blueprint.route('/accounts/password-reset-complete/')
@login_required
def accounts_password_reset_complete():
    return render_template('accounts/password_reset_complete.html', segment='password-reset-complete', parent='accounts')

@blueprint.route('/accounts/password-reset-done/')
@login_required
def accounts_password_reset_done():
    return render_template('accounts/password_reset_done.html', segment='password-reset-done', parent='accounts')

@blueprint.route('/accounts/recover-password/')
@login_required
def accounts_recover_password():
    return render_template('accounts/recover-password.html', segment='recover-password', parent='accounts')



def get_segment( request ):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None

