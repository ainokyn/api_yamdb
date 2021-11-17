from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Genre(models.Model):
    """
    Genre of titles.
    One title can be linked to several genres.
    """
    name = models.CharField(max_length=200, verbose_name='Genre', unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Category of genres («Films», «Books», «Music»).
    """
    name = models.CharField(max_length=200, verbose_name='Category',
                            unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('id',)
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
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre.name} - {self.title.name}'


class Review(models.Model):
    """Description of the Reviews model."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(
        default=1, verbose_name='score',
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'date of publication review', auto_now_add=True, db_index=True)

    class Meta:
        """Function for creating a unique combination."""
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Description of the Comments model."""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE,
                                related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'date of publication comment', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
