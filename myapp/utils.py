# utils.py

from smartstudyass import settings
from django.core.mail import send_mail

# Map common carriers to their SMS gateways
CARRIER_GATEWAYS = {
    'att': 'txt.att.net',
    'verizon': 'vtext.com',
    'tmobile': 'tmomail.net',
    'sprint': 'messaging.sprintpcs.com',
    # add more if needed
}

# Function to send SMS via Email Gateway
def  send_sms(phone_number, carrier, message):
    carrier_domain = CARRIER_GATEWAYS.get(carrier.lower())
    if not carrier_domain:
        raise ValueError("Carrier not supported")

    to_email = f"{phone_number}@{carrier_domain}"
    send_mail(  # type: ignore
        subject='',  # SMS usually ignores the subject
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )

# Function to send welcome email
# def send_welcome_email(to_email, username):
#     subject = 'Welcome to SmartStudy'
#     message = f"Hi {username},\n\nWelcome to SmartStudy! We're glad to have you on board."
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[to_email],
#         fail_silently=False,
#     )
def send_welcome_email(to_email, username,request=None):
    subject = 'Welcome to SmartStudy'
    text_content = f"Hi {username},\n\nWelcome to SmartStudy! We're glad to have you on board."
    html_content = f"""
    <html>
        <body>
            <p>Hi <strong>{username}</strong>,</p>
            <p>Welcome to <strong>SmartStudy</strong>! We're glad to have you on board.</p>
        </body>
    </html>
    """

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
    except Exception as e:
        # Optionally log the error or handle it gracefully
        print(f"Error sending welcome email: {e}")