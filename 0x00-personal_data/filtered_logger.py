#!/usr/bin/env python3
"""Use of regex in replacing occurrences of certain field values"""

from typing import List
import re
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initiate the RedactingFormatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """return filtered values from log records"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """return a message with important info obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """creates a logger
    then returns it as an object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    target_handler = logging.StreamHandler()
    target_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))
    target_handler.setFormatter(formatter)

    logger.addHandler(target_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connection object to database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    my_db = mysql.connector.connection.MySQLConnection(host=host,
                                                       user=username,
                                                       password=password,
                                                       database=database)
    return my_db


def main() -> None:
    """return rows of users from db with sensitive data hidden"""
    my_db = get_db()
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM users;")

    titles = []
    for title in cursor.description:
        titles.append(title[0])

    logger = get_logger()

    for row in cursor:
        user_info = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, titles))
        logger.info(user_info)

    cursor.close()
    my_db.close()


if __name__ == "__main__":
    """when file is executed main will run"""
    main()
