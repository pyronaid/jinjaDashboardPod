# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import timedelta
from importlib import import_module

# import Flask
from flask import Flask, session
from flask_login import LoginManager
from flask_session import Session

from .config import Config

login_manager = LoginManager()

# App Generation
app = Flask(__name__)
# Session Conf
app.config["SESSION_PERMANENT"] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# load Configuration
app.config.from_object(Config)
# register extension
login_manager.init_app(app)

# Import routing to render the pages
module = import_module('apps.{}.routes'.format("auth_module"))
app.register_blueprint(module.blueprint)
module = import_module('apps.{}.routes'.format("dash_module"))
app.register_blueprint(module.blueprint)


#@app.before_request
#def make_session_permanent():
#    session.permanent = True
#    app.permanent_session_lifetime = timedelta(minutes=5)

