import csv
import os
import logging

from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre,
                            Review, Title,
                            TitleGenre, User)

from django.conf import settings


MODELS = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    TitleGenre: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logger.info('Импортируем данные в БД')
        for model, path in MODELS.items():
            csv_path = os.path.join(f'{settings.BASE_DIR}/static/data/{path}',)
            if model.objects.exists():
                model.objects.all().delete()
            with open(csv_path, encoding='utf8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    model.objects.create(**row)
        logger.info('Данные успешно импортированы в БД')
