# Created by Rohan at 23/01/22
from django.urls import path

from train_booking.bookings.views import BookingView,BookingCreateView,BookingDetailView
from train_booking.bookings.views import search_trains

app_name = "bookings"

urlpatterns = [
    path('search/', search_trains, name='search'),
    path('', BookingCreateView.as_view(), name="create"),
    path('bookings/', BookingView.as_view(), name="list"),
    path('bookings/<int:pk>', BookingDetailView.as_view(), name="detail")
]
