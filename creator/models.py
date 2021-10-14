import os
import re

from django.core.exceptions import ValidationError
from django.db import models


def fill_html_by_name_and_values(name, **kwargs):
    path = os.path.abspath('.') + '/creator/contents/' + name + '.html'

    if not os.path.isfile(path):
        raise FileExistsError(f'Файла %s.html не существует' % name)

    with open(path, 'r') as f:
        content = f.read()

    return content.format(**kwargs)


def validate_music_field(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename

    valid_extensions = ['.mpeg']

    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
        

class Content(models.Model):
    name = models.CharField(max_length=124)
    align = models.CharField(max_length=10)

    def content(self):
        raise NotImplementedError

    def __str__(self):
        return type(self).__name__ + f"({self.id})"


class ImageContent(Content):
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=124)

    def content(self):
        return fill_html_by_name_and_values(
            'image_content',
            image_url=self.image,
            image_description=self.description
        )


class SliderContent(Content):
    images = models.ManyToManyField(ImageContent)

    def content(self):
        #TODO: сложность в том, что контента может быть сколько угодно
        return NotImplementedError


class TextContent(Content):
    text = models.TextField()

    def content(self):
        return fill_html_by_name_and_values(
            'text_content',
            text=self.text
        )


class MusicContent(Content):
    music = models.FileField(upload_to='music/', validators=[validate_music_field])

    def content(self):
        return fill_html_by_name_and_values(
            'music_content',
            music_path=self.music
        )


class SurprizeLinkContent(Content):
    link = models.CharField(max_length=1024)

    def content(self):
        return fill_html_by_name_and_values(
            'surprize_link_content',
            surprize_link=self.link
        )


class SiteBlock(models.Model):
    name = models.CharField(max_length=124)
    order = models.IntegerField(default=0)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def to_view(self):
        contents = [ImageContent, TextContent, MusicContent, SurprizeLinkContent]

        parent_id = self.content.id

        for content_class in contents:
            view = content_class.objects.filter(id=parent_id).first()

            if view:
                return view.content()


class SurprizePassword(models.Model):
    PASSWORD_TYPES = (
        ('text', 'Любой текст'),
        ('date', 'Памятная дата'),
        ('name', 'Имя человека'),
    )

    password_type = models.CharField(max_length=4, choices=PASSWORD_TYPES)
    password = models.CharField(max_length=124)

    def value(self):
        """ В зависимости от типа """
        return ""


class SurprizeLanding(models.Model):
    keyword = models.CharField(max_length=124)
    birthday_full_name = models.CharField(max_length=128)
    password = models.ForeignKey(SurprizePassword, on_delete=models.CASCADE)
    description = models.TextField() # можно будет здесь написать от чьего имени подарок

    blocks = models.ManyToManyField(SiteBlock)

    def __str__(self):
        return self.keyword

    def to_view(self):
        """ Построить страницу по блочно """
        return "\n".join(
            [b.to_view() for b in self.blocks.all().order_by('order')]
        )


# from creator.models import ImageContent
# i = ImageContent.objects.get(id=1)
# i.content()