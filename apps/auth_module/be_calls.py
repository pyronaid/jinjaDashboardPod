# -*- encoding: utf-8 -*-
import json
import logging
from typing import cast
from types import SimpleNamespace as Namespace
from apps import Config
import requests
from requests import Response
from apps.auth_module.objects.LoginDto import LoginResponseDto, LoginRequestDto
from apps.auth_module.objects.PyronaidEncoder import PyronaidEncoder


def process_login(username_provided: str, password_hashed_provided: str) -> LoginResponseDto:
    loginResponseDto = LoginResponseDto()
    try:
        loginRequestDto = LoginRequestDto(username_provided, password_hashed_provided)
        processLoginApiResponse: Response = requests.post(Config.BE_URL + Config.BE_LOGIN_API_ADDRESS,
                                                          json.dumps(loginRequestDto, cls=PyronaidEncoder))

        loginResponseDto.responseCode = processLoginApiResponse.status_code
        if processLoginApiResponse.status_code != 200:
            logging.error("ERROR IN LOGIN PHASE")
            loginResponseDto.responseMsg = "The server answer with a code different from expected one"
        else:
            loginResponseDto = cast(LoginResponseDto,
                                    json.loads(str(processLoginApiResponse.text).replace("None", "null"),
                                               object_hook=lambda d: Namespace(**d)))
    except requests.exceptions.RequestException as e:
        logging.error("ERROR IN LOGIN PHASE")
        loginResponseDto.responseMsg = "Communication unavailable"

    return loginResponseDto
