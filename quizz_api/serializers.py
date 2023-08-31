from rest_framework import serializers

from quizz.models import Test, Question


class QuestionMixinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['pk', 'text']


class TestListSerializer(serializers.ModelSerializer):
    questions = QuestionMixinSerializer(many=True)  # создание вложенности, чтобы вопросы выводились вместе с тестом

    class Meta:
        model = Test
        exclude = ['img']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TestCreateSerializer(serializers.ModelSerializer):
    """сериализатор для создания теста"""
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = '__all__'

    def create(self, validated_data):
        questions = validated_data.pop('questions')  # получение всех вопросов которые передал пользователь

        test_instance = Test.objects.create(**validated_data)  # создание экземпляра теста
        for question in questions:
            Question.objects.create(test=test_instance, **question)  # сохранение вопросов
        return test_instance
