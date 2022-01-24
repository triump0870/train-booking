# Created by Rohan at 23/01/22
from django.core.management.base import BaseCommand

from train_booking.bookings.models import Seat
from train_booking.bookings.models import Train, Booking


class Command(BaseCommand):
    help = 'Populate the initial chart'

    def handle(self, *args, **options):
        trains = Train.objects.all()
        Seat.objects.all().delete()
        Booking.objects.all().delete()
        for train in trains:
            seat_objs = [Seat(train=train, seat_no=i + 1) for i in range(train.total_seats)]
            Seat.objects.bulk_create(seat_objs)
