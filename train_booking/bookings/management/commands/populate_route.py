# Created by Rohan at 24/01/22
from datetime import timedelta

from django.core.management.base import BaseCommand

from train_booking.bookings.models import Route


class Command(BaseCommand):
    help = 'Populate the initial chart'

    def handle(self, *args, **options):
        routes = Route.objects.all()
        for route in routes:
            counter = 1
            while counter <= 5:
                new_route = route
                new_route.pk = None
                new_route.arrival_time += timedelta(days=counter)
                new_route.departure_time += timedelta(days=counter)
                new_route.save()
                counter += 1
