from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Auditorium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('rows', models.PositiveIntegerField(default=8)),
                ('seats_per_row', models.PositiveIntegerField(default=12)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('synopsis', models.TextField()),
                ('duration_minutes', models.PositiveIntegerField()),
                ('age_rating', models.CharField(default='PG-13', max_length=10)),
                ('poster_url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Snack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.PositiveIntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='SnackOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starts_at', models.DateTimeField()),
                ('base_price', models.DecimalField(decimal_places=2, default='7.50', max_digits=8)),
                ('auditorium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.auditorium')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.movie')),
            ],
            options={'ordering': ['starts_at']},
        ),
        migrations.CreateModel(
            name='SnackOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cinema.snackorder')),
                ('snack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.snack')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('showtime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.showtime')),
            ],
        ),
        migrations.CreateModel(
            name='SeatReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.CharField(max_length=2)),
                ('number', models.PositiveIntegerField()),
                ('showtime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.showtime')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='cinema.ticket')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('showtime', 'row', 'number'), name='unique_seat_per_showtime')],
            },
        ),
    ]
