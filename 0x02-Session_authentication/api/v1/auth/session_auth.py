#!usr/bin/env python3
"""SessiomAuth class module
"""

from .auth import Auth
import uuid


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
