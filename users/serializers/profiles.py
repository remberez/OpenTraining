from users.models.profiles import *
from rest_framework import serializers
from coaching.serializers.games import GameShortSerializer, CoachingShortSerializer


class TeacherProfileSerializer(serializers.ModelSerializer):
    games = GameShortSerializer(many=True)

    class Meta:
        model = Teacher
        fields = (
            'games',
        )


class LearnerProfileSerializer(serializers.ModelSerializer):
    games = CoachingShortSerializer(many=True)

    class Meta:
        model = Learner
        fields = (
            'games',
        )
