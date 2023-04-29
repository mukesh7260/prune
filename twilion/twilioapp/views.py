from django.shortcuts import render
from rest_framework.views  import APIView
from rest_framework import status 
from twilioapp.serializers import VerifyPhoneOtpSerializer ,SendOtpToPhoneSerializer 
from rest_framework.response import Response 
from rest_framework.decorators import api_view 





# code written by mukesh 
class VerifyPhoneOtp(APIView):
        def post(self, request):
                serializer = VerifyPhoneOtpSerializer(data=request.data)
                if serializer.is_valid():
                        return Response({"detail":"PhoneOTP verified successfully"}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            
            
class PhoneViewSet(APIView):
        def post(self, request):
                serializer = SendOtpToPhoneSerializer(data=request.data)
                if serializer.is_valid():
                        return Response({ "detail":"OTP sent and will be valid for 2 minutes",},status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['GET'])
def frontent(request):
        
        
        return render(request, 'index.html')