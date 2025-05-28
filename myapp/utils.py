from django.core.mail import send_mail, EmailMultiAlternatives
import requests

from smartstudyass import settings
import logging
import time
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type # type: ignore
CARRIER_GATEWAYS = {
    'att': 'txt.att.net',
    'verizon': 'vtext.com',
    'tmobile': 'tmomail.net',
    'sprint': 'messaging.sprintpcs.com',
    # Add more carriers if needed
}

def send_sms(phone_number, carrier, message):
    carrier = carrier.strip().lower()  # Normalize carrier string
    carrier_domain = CARRIER_GATEWAYS.get(carrier)
    if not carrier_domain:
        raise ValueError(f"Carrier '{carrier}' not supported")

    to_email = f"{phone_number}@{carrier_domain}"
    send_mail(
        subject='',  # SMS gateways usually ignore the subject
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )
# Configure logging
logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
    before_sleep=lambda retry_state: logger.warning(
        f"Retrying email send (attempt {retry_state.attempt_number})..."
    )
)
def send_welcome_email(to_email, username, request=None):
    subject = 'Welcome to SmartStudy'
    text_content = f"""Hi {username},

Welcome to SmartStudy! We're thrilled to have you on board.
Explore our platform to start your learning journey with personalized courses and resources.

Best regards,
The SmartStudy Team"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Helvetica', 'Arial', sans-serif;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            background-color: #4a90e2;
            padding: 20px;
            text-align: center;
        }}
        .header img {{
            max-width: 120px;
            height: auto;
        }}
        .welcome-image {{
            width: 100%;
            max-height: 200px;
            object-fit: cover;
        }}
        .content {{
            padding: 30px;
            line-height: 1.6;
            color: #333333;
        }}
        .content h1 {{
            color: #2c3e50;
            font-size: 26px;
            margin-bottom: 20px;
        }}
        .content p {{
            margin: 0 0 15px;
            font-size: 16px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background-color: #4a90e2;
            color: #ffffff !important;
            text-decoration: none;
            border-radius: 4px;
            font-size: 16px;
            margin-top: 20px;
        }}
        .features {{
            margin: 20px 0;
        }}
        .features ul {{
            list-style-type: none;
            padding: 0;
        }}
        .features li {{
            margin-bottom: 10px;
            font-size: 15px;
        }}
        .footer {{
            background-color: #f8f8f8;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            color: #666666;
        }}
        @media only screen and (max-width: 600px) {{
            .container {{
                margin: 10px;
            }}
            .content {{
                padding: 20px;
            }}
            .welcome-image {{
                max-height: 150px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://www.freepik.com/free-photo/study-group-african-people_20147947.htm#fromView=search&page=1&position=1&uuid=c11e1849-b5da-4416-a100-45f89986a107&query=smartstudy" alt="SmartStudy Logo">
        </div>
        <img class="welcome-image" src="https://www.freepik.com/free-psd/3d-illustration-reading-with-book-esssential_171612204.htm#fromView=search&page=1&position=4&uuid=c11e1849-b5da-4416-a100-45f89986a107&query=smartstudy" alt="Welcome to SmartStudy">
        <div class="content">
            <h1>Hello, {username}!</h1>
            <p>We're thrilled to welcome you to <strong>SmartStudy</strong>! Our platform is designed to make your learning journey engaging, efficient, and tailored to your needs.</p>
            <div class="features">
                <p>Here's what you can explore:</p>
                <ul>
                    <li>📚 <strong>Personalized Courses:</strong> Curated content to match your learning goals.</li>
                    <li>📈 <strong>Progress Tracking:</strong> Monitor your achievements and stay motivated.</li>
                    <li>🌐 <strong>Community Support:</strong> Connect with learners and experts worldwide.</li>
                </ul>
            </div>
            <p>Ready to dive in? Start exploring now and unlock your potential!</p>
            <a href="https://www.smartstudy.com/get-started" class="button">Start Learning Now</a>
        </div>
        <div class="footer">
            <p>© 2025 SmartStudy. All rights reserved.</p>
            <p>Questions? Contact us at <a href="mailto:support@smartstudy.com">support@smartstudy.com</a></p>
            <p><a href="https://www.smartstudy.com/unsubscribe?email={to_email}">Unsubscribe</a></p>
        </div>
    </div>
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
        logger.info(f"Welcome email sent successfully to {to_email}")
    except Exception as e:
        logger.error(f"Error sending welcome email to {to_email}: {str(e)}")
        raise

    return subject, text_content, html_content



    # generating the key 
    import requests
from django.conf import settings

def generate_questions_from_notes(notes_text):
    api_url = "AIzaSyBsvs7VIkdlZqNxou2EP09GK-pljH1Tklg"  # Replace with actual URL
    api_key = settings.GEMINI_API_KEY

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": f"Generate 5 study questions based on the following notes:\n\n{notes_text}",
        "max_tokens": 150,  # adjust as needed
        "temperature": 0.7,  # controls creativity
    }

    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # You need to adjust this depending on API response format
        questions = data.get("choices")[0].get("text", "").strip()
        return questions
    else:
        # Log or raise error as needed
        return f"Error: {response.status_code} - {response.text}"