from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(allow_blank=True)

    class Meta:
        model = User
        fields = (
            'username',
            'discord_id',
            'email',
            'first_name',
            'last_name',
            'password',
            'is_public',
        )

    def to_representation(self, instance):
        """
        Если аккаунт публичный или запрос делает владелец аккаунта,
        то возвращаем все поля. Если аккаунт скрыт, то возвращаем
        только разрешённые поля.
        """
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.is_public or request.user == instance:
            return representation
        else:
            allowed_fields = (
                'username',
            )
            fields_to_send = {}
            for key, value in representation.items():
                if key in allowed_fields:
                    fields_to_send[key] = value
            return fields_to_send

    def validate_email(self, value):
        email = value.lower()
        if email and User.objects.filter(email=email).exists():
            raise ParseError('Email уже используется')
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_discord_id(self, value):
        if value and User.objects.filter(discord_id=value).exists():
            raise ParseError('Данный Discord ID уже используется.')
        return value

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance


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
