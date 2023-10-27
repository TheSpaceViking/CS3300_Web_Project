from django.contrib import admin
from django.apps import apps

app_name = 'gameReview_app'
app_config = apps.get_app_config(app_name)

class GameAdmin(admin.ModelAdmin):
    readonly_fields = ('overall_rating',)

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('')
    
for model in app_config.get_models():
    if model.__name__ == 'Game':
        admin.site.register(model, GameAdmin)
    else:
        admin.site.register(model)