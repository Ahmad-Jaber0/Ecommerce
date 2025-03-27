from django.core.mail import send_mail

def send_reset_email(user, request, raw_token):
    host = request.build_absolute_uri('/')
    reset_link = f"{host}api/reset_password/{raw_token}"
    
    email_body = f"""
    رابط إعادة تعيين كلمة المرور:
    {reset_link} 
    إذا لم تطلب هذا الرابط، يرجى تجاهل هذا البريد.
    """  
    send_mail(
        subject="طلب إعادة تعيين كلمة المرور",
        message=email_body,
        from_email="Ahmad@emarket.com",
        recipient_list=[user.email],
        fail_silently=False
    )