#!/usr/bin/env python3
"""function that returns the log message obfuscated"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """return a message with important info obfuscated"""
    # pattern = '|'.join(fields)
    regex = re.compile(f'("|".join(fields))=([^{separator}]*)')
    return regex.sub(fr'\1={redaction}', message)
