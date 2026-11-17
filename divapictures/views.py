from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import PhotoFrame, Order
from .serializers import FrameSerializer
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# 1. Home Page
def home(request):
    frames = PhotoFrame.objects.all()
    return render(request, 'index.html', {'frames': frames})

# 2. API ku
class FrameViewSet(viewsets.ModelViewSet):
    queryset = PhotoFrame.objects.all()
    serializer_class = FrameSerializer

# 3. NEW - Order Form Page (BUY NOW -> FORM -> PAYMENT)
def order_page(request, frame_id):
    frame = get_object_or_404(PhotoFrame, id=frame_id)
    if request.method == 'POST':
        phone = request.POST.get('phone')
        # Phone ah session la save pannurom - My Orders la avanga order mattum kaata
        request.session['customer_phone'] = phone
        Order.objects.create(
            frame=frame,
            customer_name=request.POST.get('name'),
            phone=phone,
            address=request.POST.get('address'),
            photo=request.FILES.get('photo'),
            quantity=1,
            status='Pending'
        )
        return redirect(frame.payment_link)
    
    return render(request, 'order_form.html', {'frame': frame})

# 3.5 MY ORDERS PAGE - FIXED! Customer oda order mattum kaatum
def my_orders(request):
    # Customer search panna phone, illana order pannum pothu save aana phone
    phone = request.GET.get('phone') or request.session.get('customer_phone')

    if phone:
        # +91, space lam clean panni last 10 digit mattum edukurom
        phone_clean = phone.strip().replace(' ', '').replace('+91', '')[-10:]
        # Avanga phone ku match aana order mattum!
        orders = Order.objects.filter(phone__endswith=phone_clean).order_by('-id')
        # Search panna phone ah session la save pannidu
        request.session['customer_phone'] = phone
    else:
        orders = []

    return render(request, 'orders.html', {
        'orders': orders,
        'searched_phone': phone,
        'searched': bool(phone)
    })

# 4. PAYMENT CREATE 
def create_payment(request, id):
    frame = get_object_or_404(PhotoFrame, id=id)
    amount = int(frame.price * 100)
    razorpay_order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })
    return render(request, 'payment.html', {
        'frame': frame,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': amount
    })

# 5. PAYMENT SUCCESS
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        return JsonResponse({"status": "Success"})
    return JsonResponse({"status": "Failed"})