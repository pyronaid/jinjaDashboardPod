# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from urllib.parse import parse_qs

from flask import render_template, request, redirect, flash, abort, url_for, session
from flask_login import login_user, login_required, current_user, logout_user

import apps.auth_module.be_calls as be_calls
from apps.auth_module import blueprint
from apps.auth_module.forms import LoginForm, CreateAccountForm
from apps.auth_module.models import User, convertResponseToUser
from apps.auth_module.objects.LoginDto import LoginResponseDto
from apps.auth_module.objects.SignupDto import SignupResponseDto
from apps.auth_module.util import verify_user, my_url_has_allowed_host_and_scheme, hash_pass


@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/accounts/auth-signin/', methods=['GET', 'POST'])
def accounts_signin():
    next = parse_qs(request.query_string.decode()).get('next', None)
    next = next[0] if next is not None else None
    if current_user is not None and current_user.is_authenticated:
        return redirect(next or url_for('dashboard_blueprint.index'))
    else:
        # Here we use a class of some kind to represent and validate our
        # client-side form data. For example, WTForms is a library that will
        # handle this for us, and we use a custom LoginForm to validate.
        login_form = LoginForm(request.form)
        error_username: str = None
        error_password: str = None
        error_generic: str = None
        if login_form.validate_on_submit():
            # read form data
            username = request.form['username']
            password = request.form['password']
            # Locate user
            loginResponseDto: LoginResponseDto = be_calls.process_login(username, hash_pass(password))
            if loginResponseDto is not None:
                error_username = loginResponseDto.errorMsgUsername
                error_password = loginResponseDto.errorMsgPassword
                if loginResponseDto.responseCode is not None and loginResponseDto.responseCode != 200:
                    error_generic = loginResponseDto.responseMsg
            user: User = convertResponseToUser(loginResponseDto)
            if user and verify_user(password):
                # Login and validate the user.
                # user should be an instance of your `User` class
                login_user(user)
                session[user.get_id()] = user
                flash('Logged in successfully.')
                # url_has_allowed_host_and_scheme should check if the url is safe
                # for redirects, meaning it matches the request host.
                # See Django's url_has_allowed_host_and_scheme for an example.
                next = request.args.get('next')
                if next is not None and not my_url_has_allowed_host_and_scheme(next, request.host):
                    return abort(400)
                return redirect(next or url_for('dashboard_blueprint.index'))
        return render_template('accounts/auth-signin.html', segment='signin', parent='accounts', form=login_form,
                               error_username=error_username, error_password=error_password, error_generic=error_generic)


@blueprint.route('/register', methods=['GET', 'POST'])
@blueprint.route('/accounts/auth-signup/', methods=['GET', 'POST'])
def accounts_signup():
    next = parse_qs(request.query_string.decode()).get('next', None)
    next = next[0] if next is not None else None
    if current_user is not None and current_user.is_authenticated:
        return redirect(next or url_for('dashboard_blueprint.index'))
    else:
        # Here we use a class of some kind to represent and validate our
        # client-side form data. For example, WTForms is a library that will
        # handle this for us, and we use a custom LoginForm to validate.
        create_account_form = CreateAccountForm(request.form)
        error_username: str = None
        error_password: str = None
        error_mail: str = None
        error_generic: str = None
        if create_account_form.validate_on_submit():
            # read form data
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            # Register user
            signupResponseDto: SignupResponseDto = be_calls.process_register(username, hash_pass(password), email)
            if signupResponseDto is not None:
                error_username = signupResponseDto.errorMsgUsername
                error_password = signupResponseDto.errorMsgPassword
                error_mail = signupResponseDto.errorMsgMail
                if signupResponseDto.responseCode is not None and signupResponseDto.responseCode != 200:
                    error_generic = signupResponseDto.responseMsg
            user: User = convertResponseToUser(signupResponseDto)
            if user and verify_user(password):
                # Login and validate the user.
                # user should be an instance of your `User` class
                login_user(user)
                session[user.get_id()] = user
                flash('Logged in successfully.')
                return redirect(next or url_for('dashboard_blueprint.index'))
        return render_template('accounts/auth-signup.html', segment='signup', parent='accounts',
                               form=create_account_form, error_username=error_username, error_password=error_password,
                               error_mail=error_mail, error_generic=error_generic)


# Accounts
@blueprint.route('/accounts/forgot-password/')
def accounts_forgot_password():
    return render_template('accounts/forgot-password.html', segment='forgot-password', parent='accounts')


@blueprint.route('/accounts/logged_out/')
@login_required
def accounts_logged_out():
    session.pop(current_user.get_id(), None)
    logout_user()
    return render_template('accounts/logged_out.html', segment='logged_out', parent='registration')


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
    return render_template('accounts/password_reset_complete.html', segment='password-reset-complete',
                           parent='accounts')


@blueprint.route('/accounts/password-reset-done/')
@login_required
def accounts_password_reset_done():
    return render_template('accounts/password_reset_done.html', segment='password-reset-done', parent='accounts')


@blueprint.route('/accounts/recover-password/')
@login_required
def accounts_recover_password():
    return render_template('accounts/recover-password.html', segment='recover-password', parent='accounts')


# Registration
@blueprint.route('/registration/logged_out/')
@login_required
def registration_logged_out():
    session.pop(current_user.get_id(), None)
    logout_user()
    return render_template('registration/logged_out.html', segment='logged_out', parent='registration')


@blueprint.route('/registration/password_change_done/')
@login_required
def registration_password_change_done():
    return render_template('registration/password_change_done.html', segment='password_change_done',
                           parent='registration')


@blueprint.route('/registration/password_change_form/')
@login_required
def registration_password_change_form():
    return render_template('registration/password_change_form.html', segment='password_change_form',
                           parent='registration')


def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
