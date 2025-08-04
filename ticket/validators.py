from rest_framework.validators import ValidationError


def no_numbers(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("Name should not contain numbers")