from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_phone_number(value):
    reg = re.compile('^[5][0-9]{8}$')
    if not reg.match(value.replace(" ", "")):
        raise ValidationError(_('ტელეფონის ნომერი არავალიდურია(5** *** ***)'))