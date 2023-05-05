# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, redirect
from flask_login import login_required
from jinja2  import TemplateNotFound
from apps.dash_module import blueprint

# App modules
from apps import app, login_manager

# App main route + generic routing
@blueprint.route('/', defaults={'path': 'index.html'})
@blueprint.route('/')
@login_required
def index():
    try:
        return render_template( 'pages/dashboard.html', segment='analytics', parent='dashboard')
    except TemplateNotFound:
        return render_template('pages/dashboard.html'), 404


# Pages
@blueprint.route('/pages/icons')
@login_required
def pages_icons():
    return render_template('pages/icons.html', segment='icons', parent='pages')

@blueprint.route('/pages/map')
@login_required
def pages_map():
    return render_template('pages/map.html', segment='map', parent='pages')

@blueprint.route('/pages/notifications/')
@login_required
def pages_notifications():
    return render_template('pages/notifications.html', segment='notifications', parent='pages')

@blueprint.route('/pages/tables/')
@login_required
def pages_tables():
    return render_template('pages/tables.html', segment='tables', parent='pages')

@blueprint.route('/pages/typography/')
@login_required
def pages_typography():
    return render_template('pages/typography.html', segment='typography', parent='pages')

@blueprint.route('/pages/user/')
@login_required
def pages_user():
    return render_template('pages/user.html', segment='user', parent='pages')

# Registration

@blueprint.route('/registration/logged_out/')
def registration_logged_out():
    return render_template('registration/logged_out.html', segment='logged_out', parent='registration')

@blueprint.route('/registration/password_change_done/')
@login_required
def registration_password_change_done():
    return render_template('registration/password_change_done.html', segment='password_change_done', parent='registration')

@blueprint.route('/registration/password_change_form/')
@login_required
def registration_password_change_form():
    return render_template('registration/password_change_form.html', segment='password_change_form', parent='registration')


def get_segment( request ):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None

    # Custom Filter
@app.template_filter('replace_value')
def replace_value(value, arg):
    return value.replace(arg, ' ').title()