from django.apps import apps
from django.contrib import admin

from train_booking.bookings.models import Route

# Register your models here.
models = apps.get_app_config("bookings").get_models()


class RouteAdmin(admin.ModelAdmin):
    fields = ['train', 'source', 'destination', 'arrival_time', 'departure_time']


admin.site.register(Route, RouteAdmin)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
