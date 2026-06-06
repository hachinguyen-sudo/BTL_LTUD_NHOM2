from django import forms
from .models import Booking

# Danh sách quận — dùng chung cho form và views
QUAN_CHOICES = [
    ('', '-- Chọn quận/huyện --'),
    ('Hoàn Kiếm',    'Hoàn Kiếm'),
    ('Đống Đa',      'Đống Đa'),
    ('Hai Bà Trưng', 'Hai Bà Trưng'),
    ('Ba Đình',      'Ba Đình'),
    ('Tây Hồ',       'Tây Hồ'),
    ('Cầu Giấy',     'Cầu Giấy'),
    ('Thanh Xuân',   'Thanh Xuân'),
    ('Hoàng Mai',    'Hoàng Mai'),
    ('Long Biên',    'Long Biên'),
]

TIME_SLOT_CHOICES = [
    ('', '-- Chọn khung giờ --'),
    ('07:00-09:00', '07:00 – 09:00'),
    ('09:00-11:00', '09:00 – 11:00'),
    ('13:00-15:00', '13:00 – 15:00'),
    ('15:00-17:00', '15:00 – 17:00'),
]

METHOD_CHOICES = [
    ('cash',          'Tiền mặt'),
    ('bank_transfer', 'Chuyển khoản ngân hàng'),
]


class BookingForm(forms.Form):
    # Thông tin lịch hẹn
    address      = forms.CharField(
                       max_length=200,
                       label='Địa chỉ',
                       widget=forms.TextInput(attrs={
                           'placeholder': 'Số nhà, tên đường...',
                           'class': 'form-control'
                       }))

    district     = forms.ChoiceField(
                       choices=QUAN_CHOICES,
                       label='Quận/Huyện',
                       widget=forms.Select(attrs={
                           'class': 'form-control'
                       }))

    booking_date = forms.DateField(
                       label='Ngày thực hiện',
                       widget=forms.DateInput(attrs={
                           'type': 'date',
                           'class': 'form-control'
                       }))

    time_slot    = forms.ChoiceField(
                       choices=TIME_SLOT_CHOICES,
                       label='Khung giờ',
                       widget=forms.Select(attrs={
                           'class': 'form-control'
                       }))

    note         = forms.CharField(
                       required=False,
                       label='Ghi chú',
                       widget=forms.Textarea(attrs={
                           'rows': 3,
                           'placeholder': 'Yêu cầu đặc biệt (nếu có)...',
                           'class': 'form-control'
                       }))

    # Mã khuyến mãi
    promotion_code = forms.CharField(
                         required=False,
                         label='Mã khuyến mãi',
                         widget=forms.TextInput(attrs={
                             'placeholder': 'Nhập mã nếu có...',
                             'class': 'form-control'
                         }))

    # Phương thức thanh toán
    method = forms.ChoiceField(
                 choices=METHOD_CHOICES,
                 label='Hình thức thanh toán',
                 widget=forms.RadioSelect())

    # Kiểm tra ngày đặt không được là ngày quá khứ
    def clean_booking_date(self):
        from django.utils import timezone
        booking_date = self.cleaned_data.get('booking_date')
        today = timezone.now().date()
        if booking_date < today:
            raise forms.ValidationError('Ngày đặt lịch không được là ngày trong quá khứ.')
        return booking_date

    # Kiểm tra quận hợp lệ
    def clean_district(self):
        district = self.cleaned_data.get('district')
        if not district:
            raise forms.ValidationError('Vui lòng chọn quận/huyện.')
        return district