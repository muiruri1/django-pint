import re

from django.forms.widgets import MultiWidget, Select, NumberInput

from . import ureg


class QuantityWidget(MultiWidget):

    def get_choices(self, allowed_types=None):
        allowed_types = allowed_types or dir(ureg)
        return [(x, x) for x in allowed_types]
        
    def __init__(self, attrs=None, base_units=None, allowed_types=None):
        choices = self.get_choices(allowed_types)
        self.base_units = base_units
        attrs = attrs or {}
        attrs.setdefault('step', 'any')

        widgets = (
                    NumberInput(attrs=attrs),
                    Select(attrs=attrs, choices=choices)
                )

        super(QuantityWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        non_decimal = re.compile(r'[^\d.]+')
        if value:
            number_value = non_decimal.sub('', str(value))
            return [number_value, self.base_units]
        return [None, self.base_units]
