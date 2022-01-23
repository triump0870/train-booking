from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

from train_booking.bookings.forms import BookingCreateForm
from train_booking.bookings.forms import SearchForm
from train_booking.bookings.models import Booking
from train_booking.bookings.services import search


# Create your views here.


def search_trains(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            data = search(**form.cleaned_data)
            return render(request, 'bookings/search_results.html', {"data": data})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'bookings/search.html', {'form': form})


class BookingView(ListView):
    model = Booking


class BookingCreateView(CreateView):
    model = Booking

    def get(self, request, *args, **kwargs):
        context = {'form': BookingCreateForm()}
        return render(request, 'bookings/booking_create.html', context)

    def post(self, request, *args, **kwargs):
        form = BookingCreateForm(request.POST)
        try:
            if form.is_valid():
                booking = form.save(commit=False)
                booking.save()
                return HttpResponseRedirect(reverse_lazy('bookings:detail', args=[booking.pnr]))
        except Exception as ex:
            return HttpResponse(content=f"{ex.args[0]}")
        return render(request, 'bookings/booking_create.html', {'form': form})


class BookingDetailView(DetailView):
    model = Booking
