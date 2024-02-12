#!/usr/bin/env python3
"""BasicAuth class inherits from Auth"""

from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):

    def __init__(self):
        """initilize BasicAuth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns base64 auth value or None"""
        ah = authorization_header
        if not ah or not isinstance(ah, str):
            return None
        ah_list = ah.split(" ")
        if not ah_list or ah_list[0] != "Basic" or len(ah_list) < 2:
            return None
        return ah_list[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str) -> str:
        """Returns a base64 decoded string or None"""
        bah = base64_authorization_header
        if not bah or not isinstance(bah, str):
            return None
        try:
            auth_string = base64.b64decode(bah)
            clean_string = auth_string.decode('utf-8')
        except base64.binascii.Error:
            return None
        return clean_string
