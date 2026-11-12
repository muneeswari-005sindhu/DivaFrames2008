from django.contrib import admin
from .models import PhotoFrame, Order

# Header Name Change
admin.site.site_header = "DIVA FRAMES Admin"
admin.site.site_title = "DIVA FRAMES"
admin.site.index_title = "Welcome to DIVA FRAMES Administration"

@admin.register(PhotoFrame)
class PhotoFrameAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'price', 'stock']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'frame', 'phone', 'quantity', 'total_price', 'status', 'ordered_at']
    list_filter = ['status', 'ordered_at']
    search_fields = ['customer_name', 'phone']
    list_editable = ['status']