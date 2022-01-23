from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.utils import timezone

from train_booking.bookings.models import Booking
from train_booking.bookings.models import Station


class BookingCreateForm(forms.ModelForm):
    date_of_journey = forms.DateField(label='date', widget=AdminDateWidget(attrs={"type": "date"}), required=True)

    class Meta:
        model = Booking
        fields = ['train', 'from_station', 'to_station', 'date_of_journey', 'number_of_seats']


class SearchForm(forms.Form):
    template_name = 'search_form.html'
    station_query_set = Station.objects.all()
    from_station = forms.ModelChoiceField(queryset=station_query_set, required=True)

    to_station = forms.ModelChoiceField(queryset=station_query_set, required=True)
    date = forms.DateField(widget=AdminDateWidget(attrs={"type": "date"}), required=True)
    seats = forms.IntegerField(min_value=1, required=True)

    def clean(self):
        if self.cleaned_data["from_station"] == self.cleaned_data["to_station"]:
            self._errors['to_station'] = self.error_class(['To_station has to be diffenrt than from_station'])
        if self.cleaned_data["date"] < timezone.now().date():
            self._errors['date'] = self.error_class(["date can't be in past"])

        return self.cleaned_data
