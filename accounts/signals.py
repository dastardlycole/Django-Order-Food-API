from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Forgot, Otp
from django.contrib.auth import get_user_model
from .models import Forgot
import random
from django.utils import timezone
from django.core.mail import send_mail

User = get_user_model()

def get_otp(n):
    code = "".join([str(random.choice(range(0,10))) for _ in range(n)])
    expiry_date = timezone.now() + timezone.timedelta(minutes=2)
    return code, expiry_date


@receiver(post_save, sender=User)
def send_otp(sender, instance, created, *args, **kwargs):
    
    if created:
        
        code, expiry_date = get_otp(6)
        
        Otp.objects.create(code=code, user=instance, expiry_date=expiry_date)
        
        message= f"""Welcome {instance.first_name}!
You have successfully registered on our platform. Your activation OTP is {code}.
Expires in 2 minutes 

Regards,
Ifemide"""

        send_mail(
            subject="OTP VERIFICATION CODE",
            message=message,
            from_email="operations@adubafx.com.ng",
            recipient_list=[instance.email]
        )
        
        
@receiver(post_save, sender=Forgot)
def send_otp_forgot(sender, instance, created, *args, **kwargs):
    forgetter = User.objects.get(email=instance.email_forgot)
         
    code, expiry_date = get_otp(6)
    
    Otp.objects.create(code=code, user=forgetter, expiry_date=expiry_date)
    
    message= f"""Welcome {forgetter.first_name}!
You have successfully registered on our platform. Your activation OTP is {code}.
Expires in 2 minutes 

Regards,
Ifemide"""

    send_mail(
        subject="OTP VERIFICATION CODE",
        message=message,
        from_email="Ifemide Cole",
        recipient_list=[forgetter.email]
    )
    
    