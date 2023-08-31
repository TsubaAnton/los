from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from quizz.models import Test, Question, TestResults
from quizz.services import generate_code, is_passed_test, Analytics

from quizz_api.serializers import TestListSerializer, QuestionSerializer, TestCreateSerializer


# Create your views here.

class TestViewSet(viewsets.ModelViewSet):
    """Контроллер для просмотра всех тестов , а также получение статистики по нему"""
    queryset = Test.objects.all()
    serializer_class = TestListSerializer

    def retrieve(self, request, *args, **kwargs):
        """Переопределение метода retrieve"""
        test = self.get_object()

        analytics = Analytics(test.pk)  # Инициализация класса Analytics из services.py для подсчёта и вывода аналитики
        number_passes = test.number_of_passing  # кол-во прохождений теста
        pass_rate = analytics.success_rate()  # получение процента успешности выполнения теста
        most_difficult_question = analytics.most_difficult_question()  # получение самого сложного вопроса
        print(most_difficult_question)

        return Response({'Процент успешного прохождения': pass_rate, 'Количество прохождений теста': number_passes,
                         'Самый сложный вопрос': most_difficult_question})


class TestCreateApiView(generics.CreateAPIView):
    """Контроллер для создания теста"""
    queryset = Test.objects.all()
    serializer_class = TestCreateSerializer


class AnswerQuestionView(APIView):
    """Контроллер для ответа на вопрос"""

    def post(self, request, test_pk, question_pk):
        test = Test.objects.get(pk=test_pk)  # получение текущего теста

        question = Question.objects.get(pk=question_pk, test=test_pk)  # получение текущего вопроса
        next_question = question.get_next_question(test_pk)  # получение следующего вопроса
        user_answer = request.data.get('answer')  # получение ответа пользователя
        if 'code' not in request.session:  # конструкция для мониторинга и сохранения ответов пользователя
            code = generate_code()  # генерация кода с помощью функции из services.py
            request.session['code'] = code  # запись кода в текущую сессию

            result = TestResults.objects.create(  # создание объекта TestResult
                test=test,
                session=code

            )

            result.save()
        try:  # Если код уже есть в сессии, то добавление балла пользователю исходя из ответа
            code = request.session['code']
            test_result = TestResults.objects.get(session=code)
            if next_question:  # если есть следующий вопрос
                if user_answer == question.answer:  # пользователь дал верный ответ

                    test_result.score += 1  # если ответ правильный пользователь получает балл
                    test_result.save()

                    return Response({'ответ': 'правильно', 'следующий вопрос': next_question.text,
                                     "id следующего вопроса": next_question.pk})

                else:
                    question.number_incorrect_answers += 1  # если пользователь ответил неправильно, то прибавляется кол-во неправильных ответов на текущий вопрос
                    question.save()
                    return Response({'ответ': 'неправильно', 'следующий вопрос': next_question.text,
                                     "id следующего вопроса": next_question.pk})

            else:  # если следующего вопроса нет

                test.number_of_passing += 1  # добавление к числу общих прохождений теста
                test.save()
                if user_answer == question.answer:  # пользователь дал верный ответ

                    del request.session['code']  # удаление кода из сессии

                    test_result.score += 1  # если ответ правильный пользователь получает балл
                    test_result.save()
                    is_passed_test(test_pk,
                                   code)  # если вопросы закончены , то вызов фукциии из services.py , для вычисления успешности попытки
                    return Response({'ответ': 'правильно', 'следующий вопрос': 'это был последний вопрос'})

                else:  # если ответ неверный
                    question.number_incorrect_answers += 1  # если пользователь ответил неправильно, то прибавляется кол-во неправильных ответов на текущий вопрос
                    question.save()
                    return Response({'ответ': 'неправильно', 'следующий вопрос': 'это был последний вопрос'})

        except Exception as e:
            """Если возникла ошибка , код из сессии удаляется"""
            print(e)
            del request.session['code']
            return Response({'Ошибка': 'повторите снова'})
