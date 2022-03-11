from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order,Cart
from.serializers import CartSerializer
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User=get_user_model()



        
@receiver(post_save, sender=Order)
def send_customer_message(sender, instance, created, *args, **kwargs):
    
    customer = User.objects.get(email=instance.user.email)
    ordered_list=[]
    cart = Cart.objects.filter(user=customer)
    first_serializer = CartSerializer(cart, many=True)
    if len(first_serializer.data) == 0:
        return f"Your cart is empty."
    
    
    total=0
    for i in first_serializer.data:
        ordered_list.append(i['cart_food_detail']['title'])
        total+=i['cart_food_detail']['price']
        ven=i['cart_food_detail']['user']
        vendor=User.objects.get(id=ven)
       
    
    ordered=",\n".join(ordered_list) 
    

    
   

    message= f"""Hello {customer.first_name}!
You have successfully placed an order on our platform.

You ordered from:
{vendor.first_name}

Your order:
{ordered}

Your total:
{total} naira

Contact:

Vendor email:
{vendor.email}

Vendor phone:
{vendor.phone}


Regards,
Ifemide"""

    send_mail(
        subject="Your order",
        message=message,
        from_email="Ifemide Cole",
        recipient_list=[customer.email]
    )

    vendor_message= f"""Hello {vendor.first_name}!
You have received an order on our platform.

The order came from:
{customer.first_name} {customer.last_name}

Their Phone number:
{customer.phone}

Their email:
{customer.email}

Their order:
{ordered}

Their address:
{instance.address}

Their order message:
{instance.message}

Their payment choice:
{instance.payment_choice}

Their total:
{total} naira




Regards,
Ifemide"""

    send_mail(
        subject="You received an order",
        message=vendor_message,
        from_email="Ifemide Cole",
        recipient_list=[vendor.email]
    )
    order = Order.objects.all()
    for i in order:
        i.delete()
    