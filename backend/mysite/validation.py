from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    if value < 1900:
        raise ValidationError(
            _('%(value)s is too small'),
            params={'value': value},
        )
    if value > 2021:
        raise ValidationError(
            _('%(value)s is too big'),
            params={'value': value},
        )
