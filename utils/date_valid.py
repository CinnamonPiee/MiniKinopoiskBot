import re
from datetime import datetime


def date_valid(date_string):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    if not date_pattern.match(date_string):
        return False

    try:
        datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return False

    return date_string
