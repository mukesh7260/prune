import random
from django.core.cache import cache
from django.core.mail import BadHeaderError, send_mail
from twilion.settings import DEFAULT_OTP_TTL as otp_ttl


# from .utils import MessageClient
# from firebase_dynamic_links import DynamicLinks
import logging

from django.core.exceptions import ImproperlyConfigured
from twilio.rest import Client

# from rajveer.settings import env

logger = logging.getLogger(__name__)


NOT_CONFIGURED_MESSAGE = (
    "Required enviroment variables "
    "TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN or MESSAGING_SERVICE_SID missing."
)


def load_twilio_config():
    logger.debug("Loading Twilio configuration")

    twilio_account_sid ="AC33ba250441391ea842241aed963a1ff9"
    twilio_auth_token ="498c8f98be23b708e16b627db195b260"
    twilio_number = "+14406643302"
    messaging_service_sid ="MG890afdbdc2152fd41bbbcacf990e4ef9"

    if not all([twilio_account_sid, twilio_auth_token, messaging_service_sid]):
        raise ImproperlyConfigured(NOT_CONFIGURED_MESSAGE)

    return (twilio_account_sid, twilio_auth_token, messaging_service_sid)


class MessageClient:
    def __init__(self):
        logger.debug("Initializing messaging client")

        (
            twilio_account_sid,
            twilio_auth_token,
            messaging_service_sid,
        ) = load_twilio_config()

        self.messaging_service_sid = messaging_service_sid
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)

        logger.debug("Twilio client initialized")

    def send_message(self, body, to):
        print(self.messaging_service_sid,"jhjhjhjh")
        self.twilio_client.messages.create(
            messaging_service_sid=self.messaging_service_sid,
            body=body,
            to=to,
            # media_url=['https://demo.twilio.com/owl.png']
        )

"""Common"""

def generate_otp():
    """generates random OTP"""
    otp = str(random.randint(100000, 999999))
    print(otp)
    return otp


"""Phone Notifications"""


def send_otp_to_phone(phone: str):  # Receives string ex: +91123472679
    """Sends random generated OTP to phone"""
    otp = generate_otp()
    body = f"Your verification code is: {otp}"

    message = MessageClient()
    try:
        cache.set(phone, otp, otp_ttl)
    except:
        raise ConnectionError("Redis server not running")

    try:
        print(body, phone , "86")
        message.send_message(body, phone)
    except:
        raise ConnectionError(
            {"error":[
                "Some error occured in message server.",
                "Check if your phone number is correct", 
                "Message server could be down"
                ]
            }
        )

    return otp
