# Created by Rohan at 23/01/22
from django.db import transaction
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from train_booking.bookings.models import Booking
from train_booking.bookings.models import Route
from train_booking.bookings.models import Seat
from train_booking.bookings.models import SeatAvailability
from train_booking.bookings.models import Train
from train_booking.bookings.services import get_available_seat_with_ids
from train_booking.bookings.services import get_available_seats
from train_booking.bookings.services import get_in_between_stations_for_train


@receiver(pre_save, sender=Booking)
def check_available_seats(sender, instance, **kwargs):
    with transaction.atomic(savepoint=False):
        available_seats, destination_train_route, source_stop = get_available_seats(instance.from_station,
                                                                                    instance.to_station,
                                                                                    instance.train.id,
                                                                                    instance.date_of_journey)
        instance.date_of_journey = source_stop.arrival_time

        if available_seats < instance.number_of_seats:
            raise Exception(
                f"Booking is not possible as required number of seats are "
                f"not available. Available seats are {available_seats}")
        if not destination_train_route:
            raise Exception("Booking is not possible as route is not available")


@receiver(pre_save, sender=Route)
def update_stop(sender, instance, **kwargs):
    if not instance.pk:
        route = Route.objects.filter(train=instance.train, destination=instance.source).first()
        if route:
            instance.stop_no = route.stop_no + 1


@receiver(post_save, sender=Train)
def update_stop(sender, instance, created, **kwargs):
    print("created: ", instance, created)
    Seat.objects.filter(train=instance).delete()
    if created:
        seat_objs = [Seat(train=instance, seat_no=i + 1) for i in range(instance.total_seats)]
        Seat.objects.bulk_create(seat_objs)
    else:
        seat_count = Seat.objects.filter(train=instance).count()
        print("seat_count: ", seat_count)
        if seat_count < instance.total_seats:
            difference = instance.total_seats - seat_count
            print("difference: ", difference)
            seat_objs = [Seat(train=instance, seat_no=seat_count + i + 1) for i in range(difference)]
            print("seat_objs: ", seat_objs)
            Seat.objects.bulk_create(seat_objs)
        elif seat_count > instance.total_seats:
            Seat.objects.filter(train=instance, seat_no__gt=instance.total_seats).delete()
