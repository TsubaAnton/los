import random

from quizz.models import TestResults, Question


def generate_code():
    """Функция для генерации кода , чтобы далее записать его в сессию"""
    options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'q', 'w', 'e', 'r', 't']

    code = ''.join(str(random.choice(options)) for _ in range(7))
    return code


def is_passed_test(test_pk, session_code):
    """Функция для проверки успешно ли пройден тест"""
    questions = Question.objects.filter(test=test_pk).count()  # получения кол-во всех вопросов в тесте

    instance = TestResults.objects.get(session=session_code)  # получения экземпляра текущей попытки

    result = instance.score / questions * 100  # деление правильных ответов на общее кол-во вопросов

    if round(result) >= 50:
        instance.is_passed = True
        instance.save()
    else:
        instance.is_passed = False
        instance.save()


class Analytics:
    """Класс для подсчёта аналитики для теста"""

    def __init__(self, test_pk):
        self.test_pk = test_pk

    def success_rate(self) -> float:
        """Метод для подсчёта процента успешности теста в среднем"""
        try:

            all_tests = TestResults.objects.filter(
                test=self.test_pk).count()  # получение общего кол-во попыток прохождения теста

            succeed_tests = TestResults.objects.filter(test=self.test_pk,
                                                       is_passed=True).count()  # Получение кол-во успешных попыток

            pass_rate = succeed_tests / all_tests * 100
            number = round(pass_rate, 2)  # округление числа до двух знаков после запятой
            return number

        except Exception as e:
            print(e)
            return 0

    def most_difficult_question(self) -> Question:
        """Метод для выявления самого сложного вопроса"""
        question = Question.objects.filter(test=self.test_pk).order_by(
            '-number_incorrect_answers').first()  # Фильтрация всех вопросов теста по кол-во неправильных ответов

        return question.text
