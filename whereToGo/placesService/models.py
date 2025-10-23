from django.db import models


class Place(models.Model):
    title = models.CharField('Название', max_length=200, unique=True)
    description_short = models.TextField('Короткое описание')
    description_long = models.TextField('Полное описание')

    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    image = models.ImageField('Картинка')


    position = models.PositiveIntegerField('Позиция', default=0)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['position']
