from django import forms


class SeatBookingForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    customer_email = forms.EmailField()
    selected_seats = forms.CharField(widget=forms.HiddenInput())


class SnackOrderForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    customer_email = forms.EmailField()
