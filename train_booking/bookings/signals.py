# Created by Rohan at 23/01/22
from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from train_booking.bookings.models import Availability
from train_booking.bookings.models import Booking
from train_booking.bookings.models import Route
from train_booking.bookings.services import get_available_seats
from train_booking.bookings.services import get_in_between_stations_for_train


@receiver(pre_save, sender=Booking)
def check_available_seats(sender, instance, **kwargs):
    with transaction.atomic(savepoint=False):
        available_seats, destination_train_route, source_stop = get_available_seats(instance.from_station,
                                                                                    instance.to_station,
                                                                                    instance.train.id,
                                                                                    instance.number_of_seats)
        instance.date_of_journey = source_stop.arrival_time

        if not available_seats:
            raise Exception("Booking is not possible as seats are not available")
        if not destination_train_route:
            raise Exception("Booking is not possible as route is not available")


@receiver(post_save, sender=Booking)
def update_chart_after_train_booking(sender, instance, created, **kwargs):
    if created:
        stations, _, source_stop = get_in_between_stations_for_train(instance.from_station, instance.to_station,
                                                                     instance.train.id)
        Availability.objects.filter(
            station__in=stations,
            train=instance.train).update(
            available_seats=F('available_seats') - instance.number_of_seats)


@receiver(pre_save, sender=Route)
def update_stop(sender, instance, **kwargs):
    if not instance.pk:
        route = Route.objects.filter(train=instance.train, destination=instance.source).first()
        if not route:
            instance.stop_no = 0
        else:
            instance.stop_no = route.stop_no + 1
