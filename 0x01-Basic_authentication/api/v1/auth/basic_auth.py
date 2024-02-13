#!/usr/bin/env
"""BasicAuth class module
"""

from typing import TypeVar, Tuple
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """Basic authentication class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns base64 auth value or None
        """
        ah = authorization_header
        if not ah or not isinstance(ah, str):
            return None
        ah_list = ah.split(" ")
        if not ah_list or ah_list[0] != "Basic" or len(ah_list) < 2:
            return None
        return ah_list[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Returns a base64 decoded string or None
        """
        bah = base64_authorization_header
        if not bah or not isinstance(bah, str):
            return None
        try:
            auth_string = base64.b64decode(bah)
            clean_string = auth_string.decode('utf-8')
        except base64.binascii.Error:
            return None
        return clean_string

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """Returns a tuple with two sting
        """
        dbah = decoded_base64_authorization_header
        if not dbah or not isinstance(dbah, str):
            return (None, None)
        if ":" not in dbah:
            return (None, None)
        dbah_list = dbah.split(":")
        if len(dbah_list) < 2:
            return (None, None)
        email = dbah_list[0]
        password = dbah_list[1]
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns a user or None
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        data = {'email': user_email}
        result = User.search(data)
        if not result:
            return None
        user = result[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a user or None
        """
        if not request:
            return None
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        base64_string = self.extract_base64_authorization_header(request)
        if not base64_string:
            return None
        utf8_string = self.decode_base64_authorization_header(base64_string)
        if not utf8_string:
            return None
        email, password = self.extract_user_credentials(utf_string)
        if not email or not password:
            return None
        user = self.user_object_from_credentials(email, password)
        if not user:
            return None
        return user
