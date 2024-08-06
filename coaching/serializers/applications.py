from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from coaching.models.applications import Status, Application
from common.serializers.mixins import ValidateMixin


User = get_user_model()


class StatusCRUSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            'code',
            'name',
        )


class StatusDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            'code',
        )


class ApplicationCreateSerializer(ValidateMixin, serializers.ModelSerializer):
    validation_fields = ['sender_discord']

    class Meta:
        model = Application
        fields = (
            'about_sender',
            'full_name',
            'game',
            'rating',
            'sender_discord',
            'sender',
            'status',
        )
        read_only_fields = ('sender', 'status')

    def _validate_sender_discord(self, value):
        request = self.context.get('request')
        if request:
            sender_profile_discord = request.user.discord_id
            if not value:
                raise ParseError('Нужно указать дискорд')
            elif sender_profile_discord != value and sender_profile_discord is not None:
                raise ParseError('Нельзя указать дискорд отличный от дискорда в профиле')
            elif User.objects.filter(discord_id=value).first() != request.user:
                raise ParseError('Данный дискорд уже используется')
        return value


class ApplicationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'sender',
            'manager',
            'about_sender',
            'created_at',
            'accepted_at',
            'status',
            'sender_discord',
            'full_name',
            'game',
            'rating',
        )


class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'full_name',
            'game',
            'status',
            'created_at',
        )


class ApplicationDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
        )


class ApplicationChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'status',
        )
        write_only_fields = ('status',)
