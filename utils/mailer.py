
import logging

# Configure logging to console to mock email sending
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Mailer")

def send_rejection_email(client_email: str, client_name: str, counsellor_name: str, date: str, time: str):
    """
    Mock function to simulate sending a rejection email to a client.
    In a real application, this would use an SMTP library or a service like SendGrid.
    """
    subject = "Appointment Update: Session Declined"
    body = f"""
    Hi {client_name},

    We regret to inform you that your counseling session with {counsellor_name} 
    scheduled for {date} at {time} has been declined/cancelled by the counselor.

    The associated slot has been released. You can book another session at your convenience.

    Best regards,
    Counselly Team
    """
    
    logger.info(f"--- MOCK EMAIL SENT ---")
    logger.info(f"To: {client_email}")
    logger.info(f"Subject: {subject}")
    logger.info(f"Body: {body}")
    logger.info(f"------------------------")
    
    return True
