#!/usr/bin/env python3
"""BasicAuth class inherits from Auth"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):

    def __init__(self):
        """initilize BasicAuth"""
