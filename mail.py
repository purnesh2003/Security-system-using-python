
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 465  # SSL port for Gmail
username = "pavanbasavaraj2003@gmail.com"
password = "Pavan@8055"



# Email details
sender_email = "purneshgowda2003@gmail.com"
receiver_email = "tilak5star143@gmail.com"
subject = "Test Email"
body = "This is a test email."

# Create a MIMEText object
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject

# Attach the email body to the message
msg.attach(MIMEText(body, "plain"))

try:
    # Connect to the SMTP server using SMTP_SSL
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    
    # Log in to the server with your application-specific password
    server.login(username, password)
    
    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())
    
    print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the connection to the server
    server.quit()
