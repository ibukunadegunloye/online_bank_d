from django.core.exceptions import ValidationError
import random



def initial_deposit_minimum(value):
    if value < 100:
        raise ValidationError("Initial deposit must be at least N1000.")

