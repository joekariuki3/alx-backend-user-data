#!/usr/bin/env python3
"""DB module
"""
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to thr db with provided email and hashed password
        Returns User object
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user with arguments key:value passed
        Returns user object found
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, id: int, **kwargs) -> None:
        """updates user with the id passed with values in kwargs
        """
        user = self.find_user_by(id=id)
        session = self._session
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError()
            user.key = value
        session.commit()
