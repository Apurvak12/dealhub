import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import EmailProductInfo, EmailContent, Notification # Ensure these types are defined in utils

class Notification:
    WELCOME = 'WELCOME'
    CHANGE_OF_STOCK = 'CHANGE_OF_STOCK'
    LOWEST_PRICE = 'LOWEST_PRICE'
    THRESHOLD_MET = 'THRESHOLD_MET'

def generate_email_body(product: EmailProductInfo, notification_type: Notification):
    THRESHOLD_PERCENTAGE = 40
    # Shorten the product title
    shortened_title = f"{product.title[:20]}..." if len(product.title) > 20 else product.title

    subject = ""
    body = ""

    if notification_type == Notification.WELCOME:
        subject = f"Welcome to Price Tracking for {shortened_title}"
        body = f"""
        <div>
          <h2>Welcome to DealHUB 🚀</h2>
          <p>You are now tracking {product.title}.</p>
          <p>Here's an example of how you'll receive updates:</p>
          <div style="border: 1px solid #ccc; padding: 10px; background-color: #f8f8f8;">
            <h3>{product.title} is back in stock!</h3>
            <p>We're excited to let you know that {product.title} is now back in stock.</p>
            <p>Don't miss out - <a href="{product.url}" target="_blank" rel="noopener noreferrer">buy it now</a>!</p>
            <img src="https://i.ibb.co/pwFBRMC/Screenshot-2023-09-26-at-1-47-50-AM.png" alt="Product Image" style="max-width: 100%;" />
          </div>
          <p>Stay tuned for more updates on {product.title} and other products you're tracking.</p>
        </div>
        """
    elif notification_type == Notification.CHANGE_OF_STOCK:
        subject = f"{shortened_title} is now back in stock!"
        body = f"""
        <div>
          <h4>Hey, {product.title} is now restocked! Grab yours before they run out again!</h4>
          <p>See the product <a href="{product.url}" target="_blank" rel="noopener noreferrer">here</a>.</p>
        </div>
        """
    elif notification_type == Notification.LOWEST_PRICE:
        subject = f"Lowest Price Alert for {shortened_title}"
        body = f"""
        <div>
          <h4>Hey, {product.title} has reached its lowest price ever!!</h4>
          <p>Grab the product <a href="{product.url}" target="_blank" rel="noopener noreferrer">here</a> now.</p>
        </div>
        """
    elif notification_type == Notification.THRESHOLD_MET:
        subject = f"Discount Alert for {shortened_title}"
        body = f"""
        <div>
          <h4>Hey, {product.title} is now available at a discount more than {THRESHOLD_PERCENTAGE}%!</h4>
          <p>Grab it right away from <a href="{product.url}" target="_blank" rel="noopener noreferrer">here</a>.</p>
        </div>
        """
    else:
        raise ValueError("Invalid notification type.")

    return EmailContent(subject=subject, body=body)

def send_email(email_content: EmailContent, send_to: list):
    # Email configuration
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    sender_email = 'javascriptmastery@outlook.com'
    password = os.getenv('EMAIL_PASSWORD')

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(send_to)
    msg['Subject'] = email_content.subject

    # Attach body to message
    msg.attach(MIMEText(email_content.body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade to a secure connection
            server.login(sender_email, password)
            server.send_message(msg)
            print('Email sent successfully.')
    except Exception as e:
        print(f"An error occurred: {e}")
