from django.core.exceptions import ValidationError


def validate_file_size(value):
    file_size = value.size
    if file_size > 2621440:
        raise ValidationError("The maximum file size that can be uploaded is 2.5MB")
    else:
        return value
