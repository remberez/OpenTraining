from rest_framework import serializers
from rest_framework.exceptions import ParseError
from coaching.models.games import Game, GameGenre
from common.serializers.mixins import ValidateMixin


class ValidateGameMixin(ValidateMixin):
    validation_fields = (
        'name',
    )

    def _validate_name(self, value):
        return self.exists_validate(value, 'name')


class GameShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'id',
            'name',
        )


class GameListAndRetrieveSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    count_teachers = serializers.IntegerField(default=None)
    genre = serializers.CharField()

    class Meta:
        model = Game
        fields = (
            'pk',
            'name',
            'description',
            'image',
            'genre',
            'count_teachers'
        )


class CreateGameSerializer(ValidateGameMixin, serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'pk',
            'name',
            'description',
            'image',
            'genre'
        )


class DeleteGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('pk',)


class GameUpdateSerializer(ValidateGameMixin, serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Game
        fields = (
            'name',
            'description',
            'image',
        )

    def validate(self, attrs):
        if not attrs:
            raise ParseError('Введите хотя бы одно поле')

        attrs = super().validate(attrs)
        return attrs


class GameGenreRetrieveListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGenre
        fields = (
            'pk',
            'name',
        )


class GameGenreDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGenre
        fields = (
            'pk',
        )


class GameGenreUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGenre
        fields = (
            'name',
        )


class GameGenreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGenre
        fields = (
            'name',
        )
