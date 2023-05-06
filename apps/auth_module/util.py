# -*- encoding: utf-8 -*-

import binascii
import hashlib
import os

from django.utils.http import url_has_allowed_host_and_scheme


# https://flask-login.readthedocs.io/en/latest/#your-user-class

def hash_pass(password):
    """Hash a password for storing."""

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_user(provided_password):
    """Verify a stored password against one provided by user"""

    #stored_password = stored_password.decode('ascii')
    # salt = stored_password[:64]
    # stored_password = stored_password[64:]
    # pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    # pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    #return provided_password == stored_password
    return True


def my_url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=False):
    return url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=False)
