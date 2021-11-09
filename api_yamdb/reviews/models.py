from django.db import models


class Genre(models.Model):
    """
    Genre of titles.
    One title can be linked to several genres.
    """
    name = models.CharField(max_length=200, verbose_name='Genre', unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Category of genres («Films», «Books», «Music»).
    """
    name = models.CharField(max_length=200, verbose_name='Category', unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Genres with users reviews.
    """
    name = models.CharField(max_length=200, verbose_name='Title')
    year = models.IntegerField(
        verbose_name='Year of publishing',
        blank=True,
        null=True,
    )
    description = models.TextField(
        max_length=200,
        verbose_name='Description',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='genre',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
    )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name
