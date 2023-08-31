from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Test(models.Model):
    img = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    name = models.CharField(verbose_name='название теста', max_length=100)
    description = models.TextField(verbose_name='описание теста', **NULLABLE)
    number_of_passing = models.PositiveIntegerField(default=0, verbose_name='количество прохождений')


class Question(models.Model):
    answer_choices = [
        ('yes', 'yes'),
        ('no', 'no')
    ]

    text = models.TextField(verbose_name='текст вопроса')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='тест к которому принадлежит вопрос',
                             related_name='questions',
                             **NULLABLE)

    answer = models.CharField(max_length=3, verbose_name='ответ', choices=answer_choices, default='no')
    number_incorrect_answers = models.PositiveIntegerField(default=0, verbose_name='количество неправильных ответов')

    def __str__(self):
        return f'{self.text}'

    def get_next_question(self, test_pk):
        """Метод для получения следующего вопроса"""
        next_question = Question.objects.filter(pk__gt=self.pk, test=test_pk).first()
        return next_question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class TestResults(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест', **NULLABLE)
    is_passed = models.BooleanField(default=False, verbose_name='Пройден')
    session = models.CharField(max_length=7, verbose_name='ключ сессии', unique=True)
    score = models.PositiveIntegerField(verbose_name='результат пользователя', default=0)

    def __str__(self):
        return f'{self.test}'

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты теста'
