from django.db import models
import tinymce.models as tinymce_models

class Place(models.Model):
    title = models.CharField('Название', max_length=200, unique=True)
    description_short = models.TextField('Короткое описание')
    description_long = tinymce_models.HTMLField('Полное описание')

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
    image = models.ImageField('Картинка', upload_to='place_images/')

    sort_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f"Фотография {self.id} для {self.place.title}"
