from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Создание кастомной команды для создания админа, так как модель регистрации переопределена """

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@gmail.ru',
            first_name='admin',
            last_name='adminov',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password('1234')
        user.save()
