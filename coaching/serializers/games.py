from rest_framework import serializers
from coaching.models.coaching import Coaching
from coaching.models.games import Game


class GameShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'pk',
            'name',
        )


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

    class Meta:
        model = Coaching
        fields = (
            'pk',
            'game',
        )

    def to_representation(self, instance):
        fields = super().to_representation(instance)
        fields['game'] = Game.objects.filter(pk=int(fields['game'])).first().__str__()
        return fields
