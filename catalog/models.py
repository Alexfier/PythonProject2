from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    content = models.TextField(null=True, blank=True, verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/preview',
                                null=True, blank=True, verbose_name='изображение',
                                help_text='Загрузите изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=False, verbose_name='признак публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.title