from django.contrib import admin
from django.apps import apps
from .models import Publisher

app_name = 'gameReview_app'
app_config = apps.get_app_config(app_name)

class GameAdmin(admin.ModelAdmin):
    readonly_fields = ('overall_rating',)
    
    
class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('')

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Publisher, PublisherAdmin)

for model in app_config.get_models():
    if model.__name__ == 'Game':
        admin.site.register(model, GameAdmin)
    elif model.__name__ != 'Publisher':
        admin.site.register(model)