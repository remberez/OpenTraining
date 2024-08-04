from users.models.profiles import *
from rest_framework import serializers
from coaching.serializers.games import GameShortSerializer
from coaching.serializers.coaching import CoachingShortSerializer


class TeacherProfileSerializer(serializers.ModelSerializer):
    games_taught = GameShortSerializer(many=True)

    class Meta:
        model = Teacher
        fields = (
            'games_taught',
        )


class LearnerProfileSerializer(serializers.ModelSerializer):
    learning_games = CoachingShortSerializer(many=True)

    class Meta:
        model = Learner
        fields = (
            'learning_games',
        )
