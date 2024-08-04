from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ParseError


class ValidateMixin:
    validation_fields = None

    def validate(self, attrs):
        """
        Сделано для того, что бы возвращать сразу все
        ошибки валидации полей, а не только ошибку первого поля,
        которое не прошло валидацию.
        """
        validation_errors = []
        for field in self.validation_fields:
            validator = '_validate_' + field
            if hasattr(self, validator):
                try:
                    value = attrs.get(field)
                    getattr(self, validator)(value)
                except ParseError as e:
                    validation_errors.append(e)
                except ValidationError as e:
                    validation_errors.append(e)
        if validation_errors:
            raise serializers.ValidationError(validation_errors)
        return attrs

    def exists_validate(self, value, field):
        model = self.Meta.model
        if value and model.objects.filter(**{field: value}).exists():
            raise ParseError(field + ' уже используется')
        return value
