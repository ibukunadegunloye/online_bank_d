from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

def validate_min_length(value):
    if len(value) < 6:
        raise ValidationError('PIN must be at least 6 characters long.')



class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified)


generate_token = TokenGenerator()