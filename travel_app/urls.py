from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.SignUp, name="signup"),
    path("logout/", views.form_logout, name="logout"),
    path("login/", views.Login, name="login"),
    path("book/<int:pk>/", views.book, name="book"),
    path("bookings/", views.my_bookings, name="bookings"),
    path("cancel_booking/<int:pk>/", views.cancel_booking, name="cancel_booking"),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.update_profile, name="update_profile"),
    path("confirmation/<int:pk>/", views.booking_confirmation, name="confirmation"),
    path("generate_pdf/<int:booking_id>/", views.generate_pdf, name="generate_pdf")
]   
