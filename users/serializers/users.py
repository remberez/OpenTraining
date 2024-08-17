from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from common.serializers.mixins import ValidateMixin
from coaching.serializers.coaching import TeacherGameSerializer

User = get_user_model()


class UserValidate(ValidateMixin):

    def _validate_email(self, value):
        if value:
            email = value.lower()
            return self.exists_validate(email, 'email')

    def _validate_discord_id(self, value):
        return self.exists_validate(value, 'discord_id')

    def _validate_username(self, value):
        return self.exists_validate(value, 'username')


class UserRegistrationSerializer(UserValidate, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)
    discord_id = serializers.CharField(required=False)
    username = serializers.CharField(required=False)

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

    def _validate_password(self, value):
        validate_password(value)
        return value

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


class PartialUpdateUserSerializer(UserValidate, serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    discord_id = serializers.CharField(required=False)
    username = serializers.CharField(required=False)

    validation_fields = (
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
            'is_public',
        )


class TeacherSerializer(serializers.ModelSerializer):
    games_taught = TeacherGameSerializer(many=True, source='teachers_game')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'discord_id',
            'name',
            'image',
            'games_taught',
        )
