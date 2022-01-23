from django.apps import apps
from django.contrib import admin

# Register your models here.
models = apps.get_app_config("bookings").get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
