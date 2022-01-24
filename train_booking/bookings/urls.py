# Created by Rohan at 23/01/22
from django.urls import path

from train_booking.bookings.views import BookingCreateView
from train_booking.bookings.views import BookingDetailView
from train_booking.bookings.views import BookingView
from train_booking.bookings.views import search_trains, RouteListView

app_name = "bookings"

urlpatterns = [
    path('search/', search_trains, name='search'),
    path('', BookingCreateView.as_view(), name="create"),
    path('bookings/', BookingView.as_view(), name="list"),
    path('bookings/<int:pk>', BookingDetailView.as_view(), name="detail"),
    path('routes/', RouteListView.as_view(),name="route_list"),

]
