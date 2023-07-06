import csv
import os

from django.core.management import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import (User, Category,
                            Genre, Title,
                            Comment, Review, TitleGenre)


class Command(BaseCommand):

    def import_user(self):
        csv_path = os.path.join(BASE_DIR / 'static/data/users.csv')
        if User.objects.exists():
            User.objects.all().delete()
        with open(csv_path, encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )

    def import_category(self):
        csv_path = os.path.join(BASE_DIR / 'static/data/category.csv')
        if Category.objects.exists():
            Category.objects.all().delete()
        with open(csv_path, encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

    def import_genre(self):
        csv_path = os.path.join(BASE_DIR / 'static/data/genre.csv')
        if Genre.objects.exists():
            Genre.objects.all().delete()
        with open(csv_path, encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

    def import_title(self):
        csv_path = os.path.join(BASE_DIR / 'static/data/titles.csv')
        if Title.objects.exists():
            Title.objects.all().delete()
        with open(csv_path, encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Title.objects.create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(id=row['category']),
                )

    def import_genre_title(self):
        csv_path = os.path.join(BASE_DIR / 'static/data/genre_title.csv')
        if TitleGenre.objects.exists():
            TitleGenre.objects.all().delete()
        with open(csv_path, encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                TitleGenre.objects.create(
                    id=row['id'],
                    genre_id=row['genre_id'],
                    title_id=row['title_id'],
                )

    def import_reviews(self):
        csv_path = os.path.join(BASE_DIR / 'static/data/review.csv')
        if Review.objects.exists():
            Review.objects.all().delete()
        with open(csv_path, encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Review.objects.create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )

    def import_comments(self):
        csv_path = os.path.join(BASE_DIR / 'static/data/comments.csv')
        if Comment.objects.exists():
            Comment.objects.all().delete()
        with open(csv_path, encoding='utf8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Comment.objects.create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date'],
                )

    def handle(self, *args, **kwargs):
        self.import_user()
        self.import_category()
        self.import_genre()
        self.import_title()
        self.import_genre_title()
        self.import_reviews()
        self.import_comments()
        print('Данные были успешно портированы')
