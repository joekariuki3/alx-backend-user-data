#!/usr/bin/env python3
""" Auth class """

from flask import request
from typing import List, TypeVar


class Auth:

    def __init__(self):
        """initilization of Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns True:
                if Check path need authentication
           else:
               returns False"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header if it has value"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """"""
        return None
