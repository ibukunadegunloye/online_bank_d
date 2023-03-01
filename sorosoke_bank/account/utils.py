from django.core.exceptions import ValidationError


def validate_min_length(value):
    if len(value) < 6:
        raise ValidationError('PIN must be at least 6 characters long.')

