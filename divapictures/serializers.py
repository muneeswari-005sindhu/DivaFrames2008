from rest_framework import serializers
from .models import PhotoFrame
class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoFrame
        fields = ['id', 'name', 'size', 'price', 'image']