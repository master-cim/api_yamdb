from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())


class User(AbstractUser):
    username = models.CharField(max_length=100,
                                blank=False,
                                null=False
                                )
    email = models.EmailField(max_length=254,
                              blank=False,
                              null=False
                              )
    role = models.CharField(max_length=100,
                            blank=False,
                            null=False
                            )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    first_name = models.CharField(max_length=100,
                                  blank=True
                                  )
    last_name = models.CharField(max_length=100,
                                 blank=True
                                 )

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            blank=False,
                            null=False
                            )
    slug = models.SlugField(unique=True,
                            blank=False,
                            null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            blank=False,
                            null=False)
    slug = models.SlugField(unique=True,
                            blank=False,
                            null=False)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200,
                            blank=False,
                            null=False)
    year = models.IntegerField(
        ('year'),
        validators=[MinValueValidator(0),
                    max_value_current_year],
        blank=False,
        null=False
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        null=True,
        default='Без категории',
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title_id = models.ForeignKey(
        'Titles',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='title'
    )
    genre_id = models.ForeignKey(
        'Genre',
        on_delete=models.SET_DEFAULT,
        null=True,
        default='Без жанра',
        related_name='genre'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title_id = models.ForeignKey(
        'Titles',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="reviews")
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title_id', 'author'],
                                    name='unique_review')
        ]


class Comments(models.Model):
    review_id = models.ForeignKey('Review',
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  null=False,
                                  related_name="comments")
    text = models.TextField(blank=False,
                            null=False,)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="comments")
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True)

    def __str__(self):
        return self.text[:15]
