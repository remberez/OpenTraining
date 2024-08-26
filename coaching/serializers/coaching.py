import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from coaching.models.coaching import Coaching, TeacherGame
from coaching.serializers.games import GameShortSerializer
from users.constants import positions

User = get_user_model()


class CoachingRetrieveSerializer(serializers.ModelSerializer):
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


class CoachingShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coaching
        fields = (
            'pk',
            'teacher',
            'learner',
            'game',
        )


class UserCoachingSerializer(serializers.ModelSerializer):
    teacher_coaching = CoachingShortInfoSerializer(read_only=True, many=True)
    learner_coaching = CoachingShortInfoSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'teacher_coaching',
            'learner_coaching',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = kwargs['context'].get('request')
        include_teacher = request.query_params.get('include_teacher', 'true') in ['true', 'True', 1]
        include_learner = request.query_params.get('include_learner', 'true') in ['true', 'True', 1]

        if not include_teacher:
            self.fields.pop('teacher_coaching')
        if not include_learner:
            self.fields.pop('learner_coaching')


class StartCoachingSerializer(serializers.ModelSerializer):
    receiver = serializers.CharField(write_only=True)

    class Meta:
        model = Coaching
        fields = (
            'receiver',
            'game',
        )

    def create(self, validated_data):
        receiver = User.objects.filter(
            username=validated_data.pop('receiver')
        ).first()

        if not receiver:
            raise ParseError('Пользователя не существует')

        request = self.context.get('request')
        sender = request.user

        role_mapping = {
            (positions.TEACHER_CODE, positions.LEARNER_CODE): {
                'learner': receiver,
                'teacher': sender,
                'teacher_consent': True,
                'learner_consent': False,
            },
            (positions.LEARNER_CODE, positions.TEACHER_CODE): {
                'learner': sender,
                'teacher': receiver,
                'teacher_consent': False,
                'learner_consent': True,
            },
        }

        data = role_mapping.get((sender.position.code, receiver.position.code))

        if not data:
            raise ParseError('Error')

        data.update({
            'start_coaching': datetime.datetime.now(),
            'is_active': True,
        })

        validated_data.update(data)
        return super().create(validated_data)


class TeacherGameSerializer(serializers.ModelSerializer):
    game = GameShortSerializer()

    class Meta:
        model = TeacherGame
        fields = (
            'game',
            'description',
            'price',
            'rating',
        )
