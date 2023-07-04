from datetime import datetime as dt
from django.core.exceptions import ValidationError


def validate_year(value):
    current_dt = dt.now()
    if value > (current_dt.year):
        raise ValidationError(
            (f'Указанный год {value} больше текущего'),
            params={'value': value},
        )
