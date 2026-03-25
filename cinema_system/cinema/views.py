from django.contrib import messages
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import SeatBookingForm, SnackOrderForm
from .models import SeatReservation, Showtime, Snack, SnackOrder, SnackOrderItem, Ticket


def home(request: HttpRequest) -> HttpResponse:
    showtimes = Showtime.objects.select_related('movie', 'auditorium').filter(starts_at__gte=timezone.now())[:12]
    return render(request, 'cinema/home.html', {'showtimes': showtimes})


def showtime_detail(request: HttpRequest, showtime_id: int) -> HttpResponse:
    showtime = get_object_or_404(Showtime.objects.select_related('movie', 'auditorium'), id=showtime_id)
    taken = set(
        SeatReservation.objects.filter(showtime=showtime).values_list('row', 'number')
    )
    rows = [chr(65 + i) for i in range(showtime.auditorium.rows)]
    seats = [{
        'row': row,
        'numbers': [{
            'number': n,
            'taken': (row, n) in taken,
        } for n in range(1, showtime.auditorium.seats_per_row + 1)],
    } for row in rows]
    return render(
        request,
        'cinema/showtime_detail.html',
        {'showtime': showtime, 'seats': seats, 'form': SeatBookingForm()},
    )


def reserve_seats(request: HttpRequest, showtime_id: int) -> HttpResponse:
    showtime = get_object_or_404(Showtime, id=showtime_id)
    if request.method != 'POST':
        return redirect('showtime_detail', showtime_id=showtime.id)

    form = SeatBookingForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Datos inválidos, revisa el formulario.')
        return redirect('showtime_detail', showtime_id=showtime.id)

    seats_raw = [seat.strip() for seat in form.cleaned_data['selected_seats'].split(',') if seat.strip()]
    if not seats_raw:
        messages.error(request, 'Selecciona al menos una butaca.')
        return redirect('showtime_detail', showtime_id=showtime.id)

    parsed = []
    for seat in seats_raw:
        row = seat[0].upper()
        number = int(seat[1:])
        parsed.append((row, number))

    with transaction.atomic():
        conflict = SeatReservation.objects.select_for_update().filter(
            showtime=showtime,
            row__in=[r for r, _ in parsed],
            number__in=[n for _, n in parsed],
        )
        conflict_set = set(conflict.values_list('row', 'number'))
        if conflict_set.intersection(parsed):
            messages.error(request, 'Una o más butacas ya fueron vendidas. Intenta de nuevo.')
            return redirect('showtime_detail', showtime_id=showtime.id)

        ticket = Ticket.objects.create(
            showtime=showtime,
            customer_name=form.cleaned_data['customer_name'],
            customer_email=form.cleaned_data['customer_email'],
        )
        for row, number in parsed:
            SeatReservation.objects.create(ticket=ticket, showtime=showtime, row=row, number=number)

    total = showtime.base_price * len(parsed)
    messages.success(request, f'Compra realizada. Ticket #{ticket.id} total: ${total}')
    return redirect('home')


def snacks(request: HttpRequest) -> HttpResponse:
    inventory = Snack.objects.all().order_by('name')
    if request.method == 'POST':
        form = SnackOrderForm(request.POST)
        if form.is_valid():
            quantities = {}
            for snack in inventory:
                qty = int(request.POST.get(f'snack_{snack.id}', '0') or '0')
                if qty > 0:
                    if qty > snack.stock:
                        messages.error(request, f'Sin stock suficiente para {snack.name}.')
                        return redirect('snacks')
                    quantities[snack] = qty

            if not quantities:
                messages.error(request, 'Selecciona al menos un producto.')
                return redirect('snacks')

            with transaction.atomic():
                order = SnackOrder.objects.create(
                    customer_name=form.cleaned_data['customer_name'],
                    customer_email=form.cleaned_data['customer_email'],
                )
                for snack, qty in quantities.items():
                    SnackOrderItem.objects.create(order=order, snack=snack, quantity=qty)
                    snack.stock -= qty
                    snack.save(update_fields=['stock'])

            messages.success(request, f'Pedido #{order.id} creado. Total ${order.total}')
            return redirect('snacks')
    else:
        form = SnackOrderForm()

    return render(request, 'cinema/snacks.html', {'snacks': inventory, 'form': form})
