from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('showtime/<int:showtime_id>/', views.showtime_detail, name='showtime_detail'),
    path('showtime/<int:showtime_id>/reserve/', views.reserve_seats, name='reserve_seats'),
    path('snacks/', views.snacks, name='snacks'),
]
