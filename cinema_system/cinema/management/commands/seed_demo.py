from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from cinema.models import Auditorium, Movie, Showtime, Snack


class Command(BaseCommand):
    help = 'Carga datos demo para el cine.'

    def handle(self, *args, **options):
        sala1, _ = Auditorium.objects.get_or_create(name='IMAX 1', defaults={'rows': 8, 'seats_per_row': 12})
        sala2, _ = Auditorium.objects.get_or_create(name='Premium 2', defaults={'rows': 7, 'seats_per_row': 10})

        movie1, _ = Movie.objects.get_or_create(
            title='Galaxia Infinita',
            defaults={
                'synopsis': 'Una tripulación rebelde lucha por salvar su planeta con efectos brutales.',
                'duration_minutes': 138,
                'age_rating': 'PG-13',
                'poster_url': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1200&auto=format&fit=crop',
            },
        )
        movie2, _ = Movie.objects.get_or_create(
            title='Noche de Acero',
            defaults={
                'synopsis': 'Acción pura en una ciudad futurista donde cada decisión cuesta caro.',
                'duration_minutes': 122,
                'age_rating': 'R',
                'poster_url': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?q=80&w=1200&auto=format&fit=crop',
            },
        )

        now = timezone.now() + timedelta(hours=2)
        showtimes = [
            (movie1, sala1, now, Decimal('9.50')),
            (movie2, sala2, now + timedelta(hours=1), Decimal('8.00')),
            (movie1, sala2, now + timedelta(days=1), Decimal('8.50')),
        ]
        for movie, auditorium, starts_at, price in showtimes:
            Showtime.objects.get_or_create(
                movie=movie,
                auditorium=auditorium,
                starts_at=starts_at,
                defaults={'base_price': price},
            )

        snacks = [
            ('Palomitas Grandes', Decimal('6.00'), 120),
            ('Nachos con Queso', Decimal('5.50'), 80),
            ('Hot Dog', Decimal('4.50'), 90),
            ('Combo Pareja', Decimal('11.00'), 50),
            ('Refresco XL', Decimal('3.50'), 150),
        ]
        for name, price, stock in snacks:
            Snack.objects.get_or_create(name=name, defaults={'price': price, 'stock': stock})

        self.stdout.write(self.style.SUCCESS('Datos demo cargados correctamente.'))
