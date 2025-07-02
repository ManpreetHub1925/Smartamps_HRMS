import smtplib
from email.message import EmailMessage

def send_password_reset_email(to_email, user_name, username, new_password):
    # Email content setup
    subject = "🔐 Password Reset Notification – SmartAmps HRMS"
    body = f"""\
        Dear {user_name},

        We received a request to reset your password for your SmartAmps HRMS account associated with this email address.

        Your new login credentials are:

        Username: {username}
        Temporary Password: {new_password}

        ⚠️ Important: For your security, please log in using the above credentials and change your password immediately from your profile settings.

        You can log in here: https://smartamps.in/hrms/login

        If you did not request this change or believe this message was sent in error, please contact our support team immediately at support@smartamps.in.

        Thank you,
        SmartAmps HRMS Team
        www.smartamps.in
        """

    # Email headers
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'no-reply@smartamps.in'  # Replace with your email
    msg['To'] = to_email

    # SMTP Configuration (example using Gmail's SMTP)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('your-email@gmail.com', 'your-app-password')  # Replace with credentials
            smtp.send_message(msg)
            print("Password reset email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)

# Example usage
send_password_reset_email(
    to_email='user@example.com',
    user_name='John Doe',
    username='johndoe',
    new_password='Temp@1234'
)
