from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView

from quizz.forms import QuestionForm, TestCreateForm, QuestionCreateForm
from quizz.models import Question, Test, TestResults
from quizz.services import generate_code, is_passed_test, Analytics


class TestsListView(ListView):
    """Контроллер для вывода всех тестов"""
    model = Test
    template_name = 'quizz/list_test.html'


def start_test(request, test_pk):
    """Контроллер для начала прохождения тестов"""
    first_question = Question.objects.filter(test=test_pk).first()  # получение первого вопроса

    if first_question:  # если вопрос есть, то пользователя перекидывает на question_view
        return redirect('quizz:questions', test_pk=test_pk, question_pk=first_question.pk)


def question_view(request, test_pk, question_pk):
    """Контроллер для прохождения теста"""
    question = Question.objects.get(pk=question_pk)  # получение текущего вопроса
    test = Test.objects.get(pk=test_pk)  # получение текущего теста

    if request.method == 'POST':

        user_answer = request.POST.get('answer')  # получение ответа пользователя
        if user_answer == question.answer:
            score = 1  # если ответ правильный пользователь получает балл
        else:
            score = 0

        if 'code' not in request.session:  # конструкция для мониторинга и сохранения ответов пользователя
            code = generate_code()  # генерация кода с помощью функции из services.py
            request.session['code'] = code  # запись кода в текущую сессию
            instance = TestResults(  # создание объекта TestResult
                test=test,
                session=code
                )
            instance.save()

        else:
            # Если код уже есть в сессии, то добавление балла пользователю исходя из ответа

            instance = TestResults.objects.get(test=test, session=request.session['code'])
            instance.score += score
            instance.save()

        # получение следующего вопроса с помощью метода модели Question
        next_question = question.get_next_question(test_pk)

        if next_question:
            # перенаправление на этот же контроллер, тоесть создание рекурсии
            return redirect('quizz:questions', test_pk=test_pk, question_pk=next_question.pk)

        else:
            # если вопросы закончены , то вызов фукциии из services.py , для вычисления успешности попытки
            is_passed_test(test_pk, request.session['code'])

            del request.session['code']  # удаление кода из сессии

            test.number_of_passing += 1  # увеличение числа прохождений текущего теста
            test.save()

        return render(request,
                      'quizz/finish.html')  # перенапрвление пользователя на шаблон, где говорится что тест закончен

    context = {
        'question': question,
        'form': QuestionForm
    }

    return render(request, 'quizz/question.html', context=context)


def create_test(request):
    """Контроллер для создания теста"""
    if request.method == 'POST':
        test_form = TestCreateForm(request.POST)
        if test_form.is_valid():
            test = test_form.save()
            return redirect('quizz:add_question',
                            test_pk=test.pk)  # если всё валидно, то перенапрвления пользователя на контроллер для добавления вопросов

    else:
        test_form = TestCreateForm()

    return render(request, 'quizz/test_create.html', {'test_form': test_form})


def add_question(request, test_pk):
    """Контроллер для создания вопросов"""
    test = Test.objects.get(pk=test_pk)

    if request.method == 'POST':
        if 'new' in request.POST:  # Если пользователь нажал на кнопку добавить вопрос

            question_form = QuestionCreateForm(request.POST)

            if question_form.is_valid():
                question = question_form.save(commit=False)
                question.test = test
                question.save()
                return redirect('quizz:add_question', test_pk=test_pk)
        else:  # Если пользователь нажал на кнопку выйти на главный экран
            return redirect('quizz:main:page')

    else:
        question_form = QuestionCreateForm()

    return render(request, 'quizz/add_question.html', {'question_form': question_form})


class TestDetail(DetailView):
    """Контроллер для выдачи аналитик по тесту"""
    model = Test
    template_name = 'quizz/statistics_page.html'

    def get_context_data(self, **kwargs):
        test = self.get_object()  # Получение текущего объекта

        statistic = Analytics(test.pk)  # Инициализация класса Analytics из services.py для подсчёта и вывода аналитики
        question = statistic.most_difficult_question()  # получение самого сложного вопроса
        pass_rate = statistic.success_rate()  # получение процента успешности выполнения теста
        context = super().get_context_data(**kwargs)
        context['number_of_passing'] = test.number_of_passing  # кол-во прохождений теста
        context['pass_rate'] = statistic.success_rate()
        context['difficult_question'] = question

        return context
