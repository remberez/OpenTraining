import pdb

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.serializers.profiles import TeacherProfileSerializer, LearnerProfileSerializer

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    discord_id = serializers.CharField()
    username = serializers.CharField()

    validation_fields = (
        'password',
        'email',
        'discord_id',
        'username',
    )

    class Meta:
        model = User
        fields = (
            'username',
            'discord_id',
            'email',
            'first_name',
            'last_name',
            'password',
        )

    def exists_validate(self, value, field):
        if value and User.objects.filter(**{field: value}).exists():
            raise ParseError(field + ' уже используется')
        return value

    def _validate_email(self, value):
        email = value.lower()
        return self.exists_validate(email, 'email')

    def _validate_password(self, value):
        validate_password(value)
        return value

    def _validate_discord_id(self, value):
        return self.exists_validate(value, 'discord_id')

    def _validate_username(self, value):
        return self.exists_validate(value, 'username')

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

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance


class UserListAndDetail(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    allowed_fields = (
        'pk',
        'username',
        'is_public',
    )

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'discord_id',
            'email',
            'first_name',
            'last_name',
            'password',
            'is_public',
        )

    def check_permissions(self, instance, fields):
        """
        Если аккаунт публичный или запрос делает владелец аккаунта,
        то возвращаем все поля. Если аккаунт скрыт, то возвращаем
        только разрешённые поля.
        """
        request = self.context.get('request')
        if instance.is_public or request.user == instance:
            return fields
        else:
            fields_to_send = {}
            for key, value in fields.items():
                if key in self.allowed_fields:
                    fields_to_send[key] = value
            return fields_to_send

    def to_representation(self, instance):

        fields = super().to_representation(instance)
        fields = self.check_permissions(instance, fields)

        if instance.is_teacher:
            fields['profile'] = TeacherProfileSerializer(instance.teacher_profile).data
        else:
            fields['profile'] = LearnerProfileSerializer(instance.learner_profile).data
        return fields


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'new_password',
            'old_password',
        )

    def validate_old_password(self, value):
        instance = self.instance
        print(value)
        if not instance.check_password(value):
            raise ParseError('Неверный пароль')
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        new_password = validated_data['new_password']
        old_password = validated_data['old_password']
        if new_password != old_password:
            instance.set_password(new_password)
            instance.save()
        return instance


class PartialUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'discord_id',
            'email',
            'first_name',
            'last_name',
            'is_public',
        )
