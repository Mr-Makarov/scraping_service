from django.db import models
import jsonfield
from scraping.utils import from_cyrillic_to_eng


def default_urls():
    return {"work_on_hh": ""}

class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Название населенного пункта",
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Язык програмирования",
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Язык програмирования'
        verbose_name_plural = 'Языки програмирования'


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык програмирования')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language")