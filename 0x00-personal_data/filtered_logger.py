#!/usr/bin/env python3
"""function that returns the log message obfuscated
    Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction -> r: a string representing by what the field
                        will be obfuscated
        message -> msg: a string representing the log line
        separator -> sep: a string representing by which character is
                          separating all fields in the log line (message)
"""

from typing import List
import re


def filter_datum(fields: List[str], r: str, msg: str, sep: str) -> str:
    """return a message with important info obfuscated"""
    return re.sub(fr'({"|".join(fields)})=[^{sep}]*',
                  lambda x: x.group(1) + "=" + r, msg)
