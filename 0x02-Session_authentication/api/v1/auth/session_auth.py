#!/usr/bin/env python3
"""SessiomAuth class module
"""

from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """SessionAuth inherits from Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session_id
        store session_id:user_id in user_id_by_session_id
        returns session_id or None
        """
        if not user_id:
            return None
        elif not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user id based on a session id
        """
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """eturns a user based on cookie value
        """
        if not request:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        if not user_id:
            return None
        user = User.get(user_id)
        if not user:
            return None
        return user
