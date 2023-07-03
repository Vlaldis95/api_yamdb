from django.core.exceptions import ValidationError
from datetime import datetime as dt


def validate_year(value):
    current_dt = dt.now()
    if value > (current_dt.year):
        raise ValidationError(
            (f'Указанный год {value} больше текущего'),
            params={'value': value},
        )
