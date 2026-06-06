from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Booking, Payment, Promotion
from .forms import BookingForm                 
from apps.services.models import Service


@login_required(login_url='login')
def booking_create_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, is_active=True)
    error   = None

    if request.method == 'POST':
        form = BookingForm(request.POST)       

        if form.is_valid():                    
            # Lấy dữ liệu đã được kiểm tra từ form
            district       = form.cleaned_data['district']
            booking_date   = form.cleaned_data['booking_date']
            time_slot      = form.cleaned_data['time_slot']
            address        = form.cleaned_data['address']
            note           = form.cleaned_data['note']
            promo_code     = form.cleaned_data['promotion_code'].strip()
            payment_method = form.cleaned_data['method']

            # Bước 2: Kiểm tra overbooking
            so_lich = Booking.objects.filter(
                booking_date=booking_date,
                time_slot=time_slot,
                status__in=['pending', 'confirmed']
            ).count()

            if so_lich >= 3:
                error = 'Khung giờ này đã kín lịch. Vui lòng chọn giờ khác.'
            else:
                # Bước 3: Kiểm tra mã khuyến mãi
                promotion = None
                if promo_code:
                    today = timezone.now().date()
                    try:
                        promotion = Promotion.objects.get(
                            code=promo_code,
                            is_active=True,
                            start_date__lte=today,
                            end_date__gte=today
                        )
                    except Promotion.DoesNotExist:
                        error = 'Mã khuyến mãi không hợp lệ hoặc đã hết hạn.'

                if not error:
                    # Bước 4: Tính tiền
                    if promotion:
                        total = service.price * (1 - promotion.discount_percent / 100)
                    else:
                        total = service.price

                    # Bước 5: Tạo Booking
                    booking = Booking.objects.create(
                        user=request.user,
                        service=service,
                        promotion=promotion,
                        address=address,
                        district=district,
                        booking_date=booking_date,
                        time_slot=time_slot,
                        note=note,
                        total_amount=total,
                        status='confirmed'
                    )

                    # Bước 6: Tạo Payment
                    Payment.objects.create(
                        booking=booking,
                        amount=booking.total_amount,
                        method=payment_method,
                        status='success',
                    )

                    return redirect('payment_success', booking_id=booking.id)
    else:
        form = BookingForm()                   

    return render(request, 'bookings/booking-form.html', {
        'service': service,
        'form':    form,                        
        'error':   error,
    })



@login_required(login_url='login')
def payment_success_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    payment = Payment.objects.get(booking=booking)
    return render(request, 'bookings/booking-success.html', {
        'booking': booking,
        'payment': payment,
    })


def search_order_view(request):
    booking = None
    error   = None
    if request.method == 'POST':
        order_id = request.POST.get('order_id', '').strip()
        phone    = request.POST.get('phone', '').strip()
        try:
            booking = Booking.objects.get(
                id=order_id,
                user__customerprofile__phone=phone
            )
        except Booking.DoesNotExist:
            error = 'Không tìm thấy đơn hàng. Vui lòng kiểm tra lại.'
    return render(request, 'bookings/search-order.html', {
        'booking': booking,
        'error':   error,
    })