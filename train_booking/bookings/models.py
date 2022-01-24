# Create your models here.
# Created by Rohan at 22/01/22
from django.db import models


class Train(models.Model):
    name = models.CharField(max_length=50, unique=True)
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=50, db_index=True, unique=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, db_index=True)
    source = models.ForeignKey(Station, on_delete=models.CASCADE, db_index=True, related_name="source")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, db_index=True, related_name="destination")
    train_charting_date = models.DateField(db_index=True)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    stop_no = models.PositiveIntegerField(blank=True, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['train', 'source', 'destination', 'arrival_time'],
                                    name="unique_route_train")
        ]

    def __str__(self):
        return f"{self.train_id}-{self.source}-{self.destination}-{self.stop_no}"


class Seat(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, db_index=True)
    seat_no = models.PositiveIntegerField(db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['train', 'seat_no'],
                                    name="unique_train_seat")
        ]

    def __str__(self):
        return f"{self.train_id}-{self.seat_no}"


class SeatAvailability(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, db_index=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_index=True)
    date = models.DateField(db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['station', 'seat', 'date'],
                                    name="unique_train_seat_station_for_date")
        ]

    def __str__(self):
        return f"{self.date}-{self.station.name}-{self.seat.seat_no}"


class Availability(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, db_index=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_index=True)
    date = models.DateField(db_index=True)
    available_seats = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['train', 'station', 'date'], name="unique_availability", )
        ]

    def __str__(self):
        return f"{self.train_id}-{self.station}-{self.available_seats}"


class Booking(models.Model):
    """
    For simplicity not including the payment status
    """
    train = models.ForeignKey(Train, on_delete=models.CASCADE, db_index=True)
    pnr = models.AutoField(primary_key=True)
    date_of_journey = models.DateTimeField()
    from_station = models.ForeignKey(Station, on_delete=models.CASCADE, db_index=True, related_name="from_station")
    to_station = models.ForeignKey(Station, on_delete=models.CASCADE, db_index=True, related_name="to_station")
    number_of_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.train_id}-{self.pnr}-{self.number_of_seats}"
