from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'train_booking.bookings'

    def ready(self):
        import train_booking.bookings.signals  # noqa
