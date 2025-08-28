from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegistrationForm, LoginForm, UpdateProfile, BookingForm
from django.contrib.auth import authenticate, login, logout
from .models import TravelOption, Booking
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import TravelOption
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required


# Create your views here.


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You must login first.")
            return redirect("login")  
        return view_func(request, *args, **kwargs)
    return wrapper



def SignUp(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, 'Signup.html', {'form':form})

def Login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "❌ Invalid username or password.")
        
    else:
        form = LoginForm(request)
    return render(request, "Login.html", {'form': form})


def form_logout(request):
    logout(request)
    return redirect("login")



def home(request):
    qs = TravelOption.objects.all()
    
    t = request.GET.get('type')
    src = request.GET.get('source')
    dest = request.GET.get('destination')
    date = request.GET.get('date')

    if t:
        qs = qs.filter(type=t)
    if src:
        qs = qs.filter(source__icontains=src)
    if dest:
        qs = qs.filter(destination__icontains=dest)
    if date:
        qs = qs.filter(date_and_time__date=date)  

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('travel_cards.html', {'travel_options': qs})
        return JsonResponse({'html': html})

    return render(request, 'home.html', {
        'travel_options': qs,
        'type_choices': TravelOption.options 
    })


@custom_login_required
def book(request, pk):
    travel_option = get_object_or_404(TravelOption, id=pk)

    if request.method == "POST":
        form = BookingForm(request.POST, travel_option=travel_option)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.travel_option = travel_option
            booking.total_price = travel_option.price * booking.number_of_seats
            booking.booking_date = timezone.now()
            booking.status = 'confirmed'
            booking.save()

            travel_option.available_seats -= booking.number_of_seats
            travel_option.save()

            return redirect("bookings")
    else:
        form = BookingForm(travel_option=travel_option)

    return render(request, 'booking.html', {"form": form, "travel_option": travel_option})

@custom_login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')

    return render(request, "bookings.html", {'bookings':bookings})

@custom_login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, id=pk, user=request.user)
    if booking.status == "confirmed":
        booking.status = "cancelled"
        booking.travel_option.available_seats += booking.number_of_seats
        booking.travel_option.save()
        booking.save()
    return redirect("bookings")

@custom_login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).select_related('travel_option')

    return render(request, 'profile.html', {'bookings': bookings})

@custom_login_required
def update_profile(request):
    if request.method == "POST":
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # <-- Keeps user logged in with updated info
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UpdateProfile(instance=request.user)

    return render(request, "profile_update.html", {"form": form})

