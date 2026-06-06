from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from apps.bookings.models import Booking, Payment
from apps.services.models import Service
from apps.reviews.models import Review, Contact


def staff_required(view_func):
    """Decorator kiểm tra quyền admin (is_staff)"""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@staff_required
def dashboard_view(request):
    today = timezone.now().date()
    
    stats = {
        'tong_booking':    Booking.objects.count(),
        'cho_xac_nhan':    Booking.objects.filter(status='pending').count(),
        'hom_nay':         Booking.objects.filter(booking_date=today).count(),
        'hoan_thanh':      Booking.objects.filter(status='done').count(),
        'tong_doanh_thu':  sum(
            p.amount for p in Payment.objects.filter(status='success')
        ),
        'chua_doc':        Contact.objects.filter(is_read=False).count(),
    }
    booking_moi = Booking.objects.order_by('-created_at')[:10]
    return render(request, 'management/dashboard.html', { 
        'stats':       stats,
        'booking_moi': booking_moi,
    })


@staff_required
def manage_orders_view(request):
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.select_related(
        'user', 'service', 'promotion'
    ).order_by('-created_at')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'management/bookings.html', {
        'bookings':      bookings,
        'status_filter': status_filter,
    })


@staff_required
def update_order_status_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'cancelled', 'done']:
            booking.status = new_status
            booking.save()
    return redirect('manage_orders')


@staff_required
def manage_services_view(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'management/services.html', {'services': services})


@staff_required
def toggle_service_view(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.is_active = not service.is_active
    service.save()
    return redirect('manage_services')


@staff_required
def manage_users_view(request):
    users = User.objects.filter(is_staff=False).select_related('customerprofile')
    return render(request, 'management/users.html', {'users': users})


@staff_required
def manage_reviews_view(request):
    reviews = Review.objects.select_related(
        'booking', 'booking__user'
    ).order_by('-created_at')
    return render(request, 'management/reviews.html', {'reviews': reviews})


@staff_required
def toggle_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_visible = not review.is_visible
    review.save()
    return redirect('manage_reviews')


#thiếu promotion.html
