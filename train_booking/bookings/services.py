from datetime import time
from typing import Type

from django.utils import timezone

from train_booking.bookings.models import Availability
from train_booking.bookings.models import Booking
from train_booking.bookings.models import Route
from train_booking.bookings.models import Seat
from train_booking.bookings.models import SeatAvailability


def get_available_stations_with_require_seats(train, stations, seats):
    available_stations_with_require_seats = Availability.objects.filter(
        train=train,
        station__in=stations, available_seats__gte=seats).order_by(
        'available_seats')
    return available_stations_with_require_seats


def get_available_seat_with_ids(train, stations, date):
    non_available_seats = SeatAvailability.objects.filter(
        seat__train=train,
        station__in=stations,
        date=date
    ).values_list('seat_id')

    available_seats = Seat.objects.filter(train=train).exclude(id__in=non_available_seats)
    return available_seats


def get_in_between_stations_for_train(from_station, to_station, train_id, date):
    destination_stop = Route.objects.filter(destination=to_station, train_id=train_id,
                                            train_charting_date=date).first()
    source_stop = Route.objects.filter(source=from_station, train_id=train_id, train_charting_date=date).first()

    if destination_stop:
        stations = (Route.objects.filter(train=destination_stop.train,
                                         stop_no__range=[source_stop.stop_no, destination_stop.stop_no],
                                         train_charting_date=date)
                    .order_by('stop_no')
                    .values_list('source'))
        return stations, destination_stop, source_stop
    return None, None


def get_available_seats(from_station, to_station, train_id, date):
    stations, destination_train_route, source_stop = get_in_between_stations_for_train(
        from_station,
        to_station,
        train_id, date)
    available_seats = 0
    if destination_train_route:
        # available_stations_with_require_seats = get_available_stations_with_require_seats(
        #     destination_train_route.train, stations, seats)
        # if available_stations_with_require_seats.count() == stations.count():
        #     available_seats = available_stations_with_require_seats.aggregate(count=Min('available_seats'))
        available_seats = get_available_seat_with_ids(destination_train_route.train, stations,
                                                      destination_train_route.train_charting_date).count()
    return available_seats, destination_train_route, source_stop


def search(from_station, to_station, date, seats):
    trains_stops_at_destination = set(Route.objects.filter(destination=to_station).values_list('train'))
    trains_in_reverse = set(Route.objects.filter(source=to_station, destination=from_station).values_list('train'))
    actual_trains = trains_stops_at_destination.difference(trains_in_reverse)

    min_time = timezone.datetime.combine(date, time.min)
    max_time = timezone.datetime.combine(date, time.max)
    trains_between_source_destination = Route.objects.filter(
        source=from_station,
        train__in=actual_trains, arrival_time__range=[min_time, max_time]) \
        .values('train', 'arrival_time')
    train_data = {"preferred": [], "non_preferred": []}
    for item in trains_between_source_destination:
        available_seats, destination_train_route, source_stop = get_available_seats(from_station, to_station,
                                                                                    item['train'], date)
        data = {
            'source': from_station,
            'destination': to_station,
            'train_no': destination_train_route.train.id,
            'train_name': destination_train_route.train.name,
            'arrival_time': item['arrival_time'].strftime("%d-%m-%Y %H:%M"),
            'available_seats': available_seats
        }
        if available_seats >= seats:
            train_data["preferred"].append(data)
        else:
            train_data["non_preferred"].append(data)

    sorted_preferred_list = sorted(train_data["preferred"], key=lambda x: x["available_seats"], reverse=True)
    sorted_non_preferred_list = sorted(train_data["non_preferred"], key=lambda x: x["available_seats"], reverse=True)
    sorted_train_data = {"preferred": sorted_preferred_list, "non_preferred": sorted_non_preferred_list}
    return sorted_train_data


def update_seat_availability(instance: Type[Booking]):
    stations, destination_stop, source_stop = get_in_between_stations_for_train(instance.from_station,
                                                                                instance.to_station,
                                                                                instance.train.id,
                                                                                instance.date_of_journey)
    available_seats = get_available_seat_with_ids(instance.train, stations, instance.date_of_journey)[
                      :instance.number_of_seats]
    seats_booked = [
        SeatAvailability(seat=seat, station_id=station_id, date=instance.date_of_journey)
        for seat in available_seats
        for station_id, in stations
    ]
    SeatAvailability.objects.bulk_create(seats_booked)
