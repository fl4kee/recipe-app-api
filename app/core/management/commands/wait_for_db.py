"""
Django command to wait for the database to be available
"""
from django.core.management import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError


class Command(BaseCommand):
    """Комманда, которая дожидается ответа от базы данных"""
    def handle(self, *args, **options):
        """Входная точка для команды."""
        # self.stdout это BaseCommand метод. Его рекомендовано использовать для вывода в командах,
        # можно использовать форматирование, перенаправлять вывод с помощью > и прочее
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                # self.check используется для системных проверок множества аспектов в джанго проекте
                # Проверяется конфигурация, зависимости и согласованность
                # разных компонентов внутри проекта
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
