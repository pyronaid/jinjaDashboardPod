# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = (os.getenv('DEBUG', 'False') == 'True')

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')
    BE_URL = os.getenv('BE_URL') + "default.svc.cluster.local"
    BE_LOGIN_API_ADDRESS = os.getenv('BE_LOGIN_API_ADDRESS')
    BE_SIGNUP_API_ADDRESS = os.getenv('BE_SIGNUP_API_ADDRESS')

    # App Config - the minimal footprint
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_9999')


    ####For local test
    #BE_URL = "http://springboot-service-extdefault.svc.cluster.local:30072"
    #BE_LOGIN_API_ADDRESS = "/authentication/login"
    #BE_SIGNUP_API_ADDRESS = "/authentication/register"