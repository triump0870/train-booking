# Created by Rohan at 23/01/22
from django.core.management.base import BaseCommand

from train_booking.bookings.models import Availability
from train_booking.bookings.models import Route
from train_booking.bookings.models import Train


class Command(BaseCommand):
    help = 'Populate the initial chart'

    def handle(self, *args, **options):
        trains = Train.objects.all()
        for train in trains:
            stations = Route.objects.filter(train=train).order_by('arrival_time').values('source', 'arrival_time')
            objs = [Availability(
                train=train,
                station_id=item["source"],
                date=item['arrival_time'].date(),
                available_seats=train.total_seats
            ) for item in stations]
            charts = Availability.objects.bulk_create(objs)
