# -*- encoding: utf-8 -*-
import json
import logging
from typing import cast
from types import SimpleNamespace as Namespace
from apps import Config
import requests
from requests import Response
from apps.auth_module.objects.LoginDto import LoginResponseDto, LoginRequestDto
from apps.auth_module.objects.SignupDto import SignupResponseDto, SignupRequestDto
from apps.auth_module.objects.PyronaidEncoder import PyronaidEncoder


def computeHeader():
    hearder = {
        'accept': 'application/json',
        'content-Type' : 'application/json',
        #'host': '104.154.118.39',
        #'content-Length': length
    }
    return hearder


def process_login(username_provided: str, password_hashed_provided: str) -> LoginResponseDto:
    loginResponseDto = LoginResponseDto()
    try:
        loginRequestDto = LoginRequestDto(username_provided, password_hashed_provided)
        processLoginApiResponse: Response = requests.post(Config.BE_URL + Config.BE_LOGIN_API_ADDRESS,
                                                          data=json.dumps(loginRequestDto, cls=PyronaidEncoder), headers=computeHeader())

        loginResponseDto.responseCode = processLoginApiResponse.status_code
        if processLoginApiResponse.status_code != 200:
            logging.error("ERROR IN LOGIN PHASE calling "+Config.BE_URL + Config.BE_LOGIN_API_ADDRESS)
            loginResponseDto.responseMsg = "The server answer with a code different from expected one"
        else:
            loginResponseDto = cast(LoginResponseDto,
                                    json.loads(str(processLoginApiResponse.text).replace("None", "null"),
                                               object_hook=lambda d: Namespace(**d)))
    except requests.exceptions.RequestException as e:
        logging.error("ERROR IN LOGIN PHASE callings "+Config.BE_URL + Config.BE_LOGIN_API_ADDRESS)
        loginResponseDto.responseMsg = "Communication unavailable"

    return loginResponseDto


def process_register(username_provided, password_hashed_provided, email_provided):
    signupResponseDto = SignupResponseDto()
    try:
        signupRequestDto = SignupRequestDto(username_provided, password_hashed_provided, email_provided)
        processSignupApiResponse: Response = requests.post(Config.BE_URL + Config.BE_SIGNUP_API_ADDRESS,
                                                          data=json.dumps(signupRequestDto, cls=PyronaidEncoder), headers=computeHeader())

        signupResponseDto.responseCode = processSignupApiResponse.status_code
        if processSignupApiResponse.status_code != 200:
            logging.error("ERROR IN SIGNUP PHASE calling "+ Config.BE_URL + Config.BE_SIGNUP_API_ADDRESS)
            signupResponseDto.responseMsg = "The server answer with a code different from expected one"
        else:
            signupResponseDto = cast(SignupResponseDto,
                                    json.loads(str(processSignupApiResponse.text).replace("None", "null"),
                                               object_hook=lambda d: Namespace(**d)))
    except requests.exceptions.RequestException as e:
        logging.error("ERROR IN SIGNUP PHASE callings "+ Config.BE_URL + Config.BE_SIGNUP_API_ADDRESS)
        signupResponseDto.responseCode = 999
        signupResponseDto.responseMsg = "Communication unavailable"

    return signupResponseDto