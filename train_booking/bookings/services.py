from datetime import time

from django.db.models import Min
from django.utils import timezone

from train_booking.bookings.models import Availability
from train_booking.bookings.models import Route


def get_available_stations_with_require_seats(train, stations, seats):
    available_stations_with_require_seats = Availability.objects.filter(
        train=train,
        station__in=stations, available_seats__gte=seats).order_by(
        'available_seats')
    return available_stations_with_require_seats


def get_in_between_stations_for_train(from_station, to_station, train_id):
    destination_stop = Route.objects.filter(destination=to_station, train_id=train_id).first()
    source_stop = Route.objects.filter(source=from_station, train_id=train_id).first()

    if destination_stop:
        stations = (Route.objects.filter(train=destination_stop.train,
                                         stop_no__range=[source_stop.stop_no, destination_stop.stop_no])
                    .order_by('stop_no')
                    .values_list('source'))
        return stations, destination_stop, source_stop
    return None, None


def get_available_seats(from_station, to_station, train_id, seats):
    stations, destination_train_route, source_stop= get_in_between_stations_for_train(from_station, to_station,
                                                                                     train_id)
    available_seats = 0
    if destination_train_route:
        available_stations_with_require_seats = get_available_stations_with_require_seats(
            destination_train_route.train, stations, seats)
        if available_stations_with_require_seats.count() == stations.count():
            available_seats = available_stations_with_require_seats.aggregate(count=Min('available_seats'))
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
    train_data = []
    for item in trains_between_source_destination:
        available_seats, destination_train_route, source_stop = get_available_seats(from_station, to_station, item['train'],
                                                                         seats)
        if available_seats:
            data = {
                'source': from_station,
                'destination': to_station,
                'train_no': destination_train_route.train.id,
                'train_name': destination_train_route.train.name,
                'arrival_time': item['arrival_time'].strftime("%d-%m-%Y %H:%M"),
                'available_seats': available_seats["count"]
            }
            train_data.append(data)
    sorted_list = sorted(train_data, key=lambda x: x["available_seats"], reverse=True)
    return sorted_list
