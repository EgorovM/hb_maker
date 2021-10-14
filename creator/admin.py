from django.contrib import admin

from creator import models

admin.site.register(models.ImageContent)
admin.site.register(models.TextContent)
admin.site.register(models.MusicContent)
admin.site.register(models.SurprizeLinkContent)
admin.site.register(models.SiteBlock)
admin.site.register(models.SurprizeLanding)
admin.site.register(models.SurprizePassword)
