from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from accounts.models import Otp, Forgot
from .signals import get_otp
from django.core.mail import send_mail

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only = True)
    class Meta:
        model = User
        fields = ['id', 'email', 'phone','first_name', 'last_name', 'password', 'is_vendor', 'is_customer','location']


class ResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    re_password = serializers.CharField(max_length=255)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)

class ForgotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forgot
        fields = ['email_forgot']

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def verify(self):
        otp = self.validated_data['otp']
        try:
            otp = Otp.objects.get(code=otp)
        except Otp.DoesNotExist:
            raise ValidationError(detail={
                "error":"Invalid OTP"
            })    
        except Exception:
            Otp.objects.filter(code=otp).delete()
            raise ValidationError(detail={
                "error":"unable to fetch OTP"
            })

        if otp.is_expired():
            raise ValidationError(detail={
                "error": "OTP expired"
            })    
        else:
            if otp.user.is_active != True:
                otp.user.is_active = True
                otp.user.save()
                return otp.user
            else:
                raise ValidationError(detail={
                    "error": "User with this OTP is already active"
                })    

class VerifyPasswordOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(max_length=255)
    re_password = serializers.CharField(max_length=255)

    def verify(self):
        otp = self.validated_data['otp']
        try:
            otp = Otp.objects.get(code=otp)
        except Otp.DoesNotExist:
            raise ValidationError(detail={
                "error":"Invalid OTP"
            })    
        except Exception:
            Otp.objects.filter(code=otp).delete()
            raise ValidationError(detail={
                "error":"unable to fetch OTP"
            })

        if otp.is_expired():
            raise ValidationError(detail={
                "error": "OTP expired"
            })    
        else:          
                return otp.user
           

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def get_new_otp(self):
        email = self.validated_data['email']

        if User.objects.filter(email=email, is_active=False).exists():
            user = User.objects.get(email=email)
            otp, expiry_date = get_otp(6)

            Otp.objects.create(code=otp, user=user, expiry_date=expiry_date)
            message = f"""Welcome {user.first_name}!
You have successfully registered on our platform. Your activation code is {otp}.
Expires in 5 minutes.

Regards,
Ifemide Cole
        """
            send_mail(
                subject="NEW OTP VERIFICATION CODE",
                message=message,
                from_email="Blog API Team",
                recipient_list=[user.email]
            )

            return {"message": "Please check your email for new OTP"}
        else:
            raise ValidationError(detail={
                "error":"unable to get inactive user with this email"
            })

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id','message','user','date_created']

# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Like
#         fields = ['post', 'like','user']