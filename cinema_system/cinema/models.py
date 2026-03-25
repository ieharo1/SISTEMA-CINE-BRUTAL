from decimal import Decimal

from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=150)
    synopsis = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    age_rating = models.CharField(max_length=10, default='PG-13')
    poster_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.title


class Auditorium(models.Model):
    name = models.CharField(max_length=50)
    rows = models.PositiveIntegerField(default=8)
    seats_per_row = models.PositiveIntegerField(default=12)

    def __str__(self) -> str:
        return self.name


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE)
    starts_at = models.DateTimeField()
    base_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('7.50'))

    class Meta:
        ordering = ['starts_at']

    def __str__(self) -> str:
        return f'{self.movie.title} - {self.starts_at:%d/%m %H:%M}'


class Ticket(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)


class SeatReservation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='seats')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    row = models.CharField(max_length=2)
    number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['showtime', 'row', 'number'],
                name='unique_seat_per_showtime',
            )
        ]


class Snack(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)

    def __str__(self) -> str:
        return self.name


class SnackOrder(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items.all()), Decimal('0'))


class SnackOrderItem(models.Model):
    order = models.ForeignKey(SnackOrder, on_delete=models.CASCADE, related_name='items')
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self) -> Decimal:
        return self.snack.price * self.quantity
