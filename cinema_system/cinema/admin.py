from django.contrib import admin

from .models import Auditorium, Movie, SeatReservation, Showtime, Snack, SnackOrder, SnackOrderItem, Ticket

admin.site.register(Movie)
admin.site.register(Auditorium)
admin.site.register(Showtime)
admin.site.register(Ticket)
admin.site.register(SeatReservation)
admin.site.register(Snack)
admin.site.register(SnackOrder)
admin.site.register(SnackOrderItem)
