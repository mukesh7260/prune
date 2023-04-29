from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .utils import send_otp_to_phone
from django.core.cache import cache



class SendOtpToPhoneSerializer(serializers.Serializer):
    country_code = serializers.CharField(max_length=3)
    phone = serializers.CharField(min_length=10,max_length=10)

    def validate_country_code(self, value):
        try:
            int(value)
            print(value)
        except:
            raise ValidationError
        return value
    
    def validate_phone(self, value):
        try:
            int(value)
        except:
            raise ValidationError
        return value

    def validate(self, attrs):
        country_code = attrs["country_code"]
        phone = attrs["phone"]

        phone_number = "+" + country_code + phone
        print(phone_number, "132")
        send_otp_to_phone(phone_number)
        return attrs





class VerifyPhoneOtpSerializer(serializers.Serializer):
    """Verifies OTP sent to phone"""
    country_code = serializers.CharField(max_length=3)
    phone = serializers.CharField(max_length=10)
    otp = serializers.CharField(write_only=True)

    def validate(self, attrs):
        country_code = attrs["country_code"]
        phone = attrs["phone"]
        otp = attrs["otp"]
        phone_number = "+" + country_code + phone
        if cache.get(phone_number) != otp:
            raise ValidationError({"errors": "Invalid OTP"})
        attrs.pop("otp")
        cache.delete(phone_number)
        return attrs
	


