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
    slug = models.SlugField(max_length=50, verbose_name='Genre_slug',
                            unique=True)

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
    slug = models.SlugField(max_length=50, verbose_name='Category_slug',
                            unique=True)

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
        verbose_name='Genre_title',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Category_title',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name='Genre_of_title')
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='title_whith_genre')

    def __str__(self) -> str:
        return f'{self.genre.name} - {self.title.name}'


class Review(models.Model):
    """Description of the Reviews model."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author_review',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='title_review',
    )
    text = models.TextField()
    score = models.IntegerField(
        default=1, verbose_name='score',
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'date of publication review', auto_now_add=True, db_index=True)

    class Meta:
        """Function for creating a unique combination."""
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Description of the Comments model."""
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='author_comment')
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='review_comment')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'date of publication comment', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text
