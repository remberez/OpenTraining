from rest_framework import serializers
from rest_framework.exceptions import ParseError
from coaching.models.games import Game
from common.serializers.mixins import ValidateMixin


class ValidateGameMixin(ValidateMixin):
    validation_fields = (
        'name',
    )

    def exists_validate(self, value, field):
        if value and Game.objects.filter(**{field: value}).exists():
            raise ParseError(field + ' уже используется')
        return value

    def _validate_name(self, value):
        return self.exists_validate(value, 'name')


class GameShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'pk',
            'name',
        )


class GameListAndRetrieveSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Game
        fields = (
            'pk',
            'name',
            'description',
            'image',
        )


class CreateGameSerializer(ValidateGameMixin, serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'pk',
            'name',
            'description',
            'image',
        )


class DeleteGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('pk',)


class ShortInfoGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id',
            'name',
        )


class GameUpdateSerializer(ValidateGameMixin, serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Game
        fields = (
            'name',
            'description',
            'image'
        )

    def validate(self, attrs):
        if not attrs:
            raise ParseError('Введите хотя бы одно поле')

        attrs = super().validate(attrs)
        return attrs
