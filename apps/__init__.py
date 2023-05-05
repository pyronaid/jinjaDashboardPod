# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

# import Flask 
from flask import Flask
from .config import Config
from flask_login import LoginManager
from importlib import import_module

login_manager = LoginManager()


# App Generation
app = Flask(__name__)
# load Configuration
app.config.from_object( Config ) 
#register extension
login_manager.init_app(app)


# Import routing to render the pages
module = import_module('apps.{}.routes'.format("auth_module"))
app.register_blueprint(module.blueprint)
module = import_module('apps.{}.routes'.format("dash_module"))
app.register_blueprint(module.blueprint)
