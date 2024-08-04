from rest_framework import serializers
from coaching.models.coaching import Coaching


class CoachingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coaching
        fields = (
            'pk',
            'teacher',
            'learner',
            'game',
            'start_coaching',
            'end_coaching',
            'is_active',
            'learner_comment',
        )


class CoachingShortSerializer(serializers.ModelSerializer):
    game = serializers.CharField()

    class Meta:
        model = Coaching
        fields = (
            'pk',
            'game',
        )
