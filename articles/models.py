
from django.db import models
from django.core.exceptions import ValidationError

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название тега')

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']

class Scope(models.Model):
    article = models.ForeignKey(Article, related_name='scopes', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='scopes', on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('article', 'is_main')  # Убедимся, что только один основной тег на статью

    def clean(self):
        if self.is_main and Scope.objects.filter(article=self.article, is_main=True).exists():
            raise ValidationError('Только один тег может быть основным для статьи.')

    def __str__(self):
        return f'{self.article.title} - {self.tag.name}'