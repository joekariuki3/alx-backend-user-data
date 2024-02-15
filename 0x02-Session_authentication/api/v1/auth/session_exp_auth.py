#!/usr/bin/env pythhon3
"""SessionExpAuth module implementation"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class implementation"""
    def __init__(self):
        session_duration = getenv("SESSION_DURATION")
        if session_duration.isdigit():
            self.session_duration = int(session_duration)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a session for user_id
        returns the session_id"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns user_id assiciated with the session_id provided
        """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            user_id = self.user_id_by_session_id[session_id]['user_id']
            return user_id
        if 'created_at' not in self.user_id_by_session_id[session_id]:
            return None
        created_at = self.user_id_by_session_id[session_id]['created_at']
        created_td = timedelta(created_at)
        duration_td = timedelta(0, 0, 0, self.session_duration, 0)
        total_time = created_td + duration_td
        if total_time < timedelta(datetime.now()):
            return None
        return user_id
