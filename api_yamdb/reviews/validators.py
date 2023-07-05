import re
from datetime import datetime as dt

from django.core.exceptions import ValidationError


def validate_year(value):
    current_dt = dt.now()
    if value > (current_dt.year):
        raise ValidationError(
            (f'Указанный год {value} больше текущего'),
            params={'value': value},
        )


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Не допустимые символы <{value}> в нике.'),
            params={'value': value},
        )
