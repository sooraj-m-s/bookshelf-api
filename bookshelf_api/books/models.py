from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Books(models.Model):
    title = models.CharField(max_length=255, unique=True)
    cover_image = models.URLField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pages = models.PositiveIntegerField()
    author = models.ForeignKey('users.Users', to_field='id', on_delete=models.CASCADE, related_name='books_written')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['published_date']),
            models.Index(fields=['is_available']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) or f"book-{self.pk}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

