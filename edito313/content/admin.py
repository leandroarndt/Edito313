from django.contrib import admin
from edito313.content import models

@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(models.Options)
