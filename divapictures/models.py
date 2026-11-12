from django.db import models

class PhotoFrame(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=10)
    image = models.ImageField(upload_to='frames/')
    payment_link = models.URLField(blank=True, null=True, help_text="GPay / PhonePe Payment Link inga paste pannunga")

    def __str__(self):
        return f"{self.name} - Stock: {self.stock}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    frame = models.ForeignKey(PhotoFrame, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='orders/', blank=True, null=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    ordered_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.frame.price * self.quantity

    def __str__(self):
        return f"{self.customer_name} - {self.frame.name} - Rs.{self.total_price}"
