import datetime
from datetime import timezone


from rest_framework import serializers
from .models import Coupon
class CouponSerialiser(serializers.ModelSerializer):
   class Meta:
       module=Coupon
       Fields=[
           'code',
           ' discount_percent',
           'active',
          'created_at',
          'expired_at',
           'used',
       ]
       read_only_fields=['used','created_at']
   def validates_discount_percent(self,value):
       if 0<= value <=100:
           raise  serializers.ValidationError("ERROR discount_percent must be between 0 and 100 ")
       return value
   def validates_expired_at(self,value):
       if value <= timezone.now():
           raise serializers.ValidationError("error expired_at cant be in the feture")
       return value
   def validate(self,data):
       if data.get("used", False):
           raise serializers.ValidationError({"used": "Cannot create coupon with used=True"})
           # optionally, ensure code format or uniqueness is handled by DB unique constraint
       return data



