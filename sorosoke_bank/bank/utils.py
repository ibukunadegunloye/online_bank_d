from django.core.exceptions import ValidationError



def initial_deposit_minimum(value):
    if value < 100:
        raise ValidationError("Initial deposit must be at least N1000.")


def validate_min_length(value):
    if len(value) < 6 or len(value) > 6:
        raise ValidationError('PIN must be 6 characters long.')
    else:
        return True




