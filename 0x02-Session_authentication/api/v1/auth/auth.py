#!/usr/bin/env python3
"""Auth class implementation
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True:
                if path not in ecluded_paths
           else:
               returns False
        """
        if path:
            if path[-1] != "/":
                path = path + "/"
        if not excluded_paths or not path or path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header if it has value
        """
        if not request:
            return None
        key = 'Authorization'
        value = request.headers.get(key)
        if not value:
            return None
        return value

    def current_user(self, request=None) -> TypeVar('User'):
        """returns a user or None
        """
        return None
