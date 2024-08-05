from rest_framework import serializers

from coaching.models.applications import Status, Application


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


class ApplicationCreateSerializer(serializers.ModelSerializer):

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


class ApplicationListSerializer(serializers.ModelSerializer):
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