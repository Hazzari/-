from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from testapp.models import *


@admin.register(Rubric)
class RubricMTTPModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 70


@admin.register(Article)
class ArticleModelsAdmin(admin.ModelAdmin):
    pass
