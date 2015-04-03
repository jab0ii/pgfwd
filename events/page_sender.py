import smtplib
import os
from email.mime.text import MIMEText
import zmq
import json
from datetime import datetime    


# Fetch the URL of the Django app
APP_URL = os.environ['APP_URL']


class PageSender:
    """
    Sends pages directly to a given contact method.
    """

    def __init__(self):
        """
        Fetches configuration for the page sender.
        """

        # Fetch SMTP configuration
        self.SMTP_SERVER = os.environ['MAILGUN_SMTP_SERVER']
        self.SMTP_PORT = int(os.environ['MAILGUN_SMTP_PORT'])
        self.SMTP_LOGIN = os.environ['MAILGUN_SMTP_LOGIN']
        self.SMTP_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
        self.APP_DOMAIN = os.environ['APP_DOMAIN']

        # Zero MQ config
        self.FUNC_TEST_ENDPOINT = os.environ['FUNC_TEST_ENDPOINT']

    def dispatch(self, user, contactIndx, eventDetails, uuid=None):
        """
        Sends a page to the user's contact method identificled by
        contactIndx. If a uuid is defined, then an ack-prompt will be sent.
        If a uuid is not defined, then an acknowledged message will be sent.

        Args:
            user (UserPCM):              user to page
            contactIndx (int):           contact method index to page
            eventDetails (EventDetails): details to put in the page
            uuid (str):                  optional, if specified, it's a 
                                         notification, else, it's an ack
                                         message
        """
        method = user.contactMethods[contactIndx]

        def _handleMessage(shorten_url):
            """
            Internal function used to determine whether or not to shorten
            the URL.
            """
            if uuid: #Page notification
                if shorten_url:
                    message = PageSender.appendAckInfo(uuid, 
                                                       user, 
                                                       eventDetails.message,
                                                       shorten_url=True)
                else:
                    message = PageSender.appendAckInfo(uuid, 
                                                       user, 
                                                       eventDetails.message)
            else: #Ack message
                message = eventDetails.message
            return message

        if method.contactType == 'email':
            message = _handleMessage(shorten_url=True)
            self._emailEndpoint(method.contactData, eventDetails.title,
                                message)
        elif method.contactType == 'sms':
            message = _handleMessage(shorten_url=True)
            self._twilioEndpoint(method.contactData, message)
        elif method.contactType == 'test':
            message = _handleMessage(shorten_url=False)
            self._zmqEndpoint(method.contactData, eventDetails.title,
                              message)
        elif method.contactType == 'gmailTest':
            message = _handleMessage(shorten_url=True)
            self._gmailEndpoint(method.contactData, eventDetails.title,
                                message)

    def _twilioEndpoint(self, phoneNumber, message):
        """
        Sends an SMS with the given parameters. 
        The from number is hard coded in the OS environment for now.
        """
        def _parseNumber(num):
            return '+1' + str(num)

        from twilio.rest import TwilioRestClient
        account = os.environ['TWILIO_ACCOUNT']
        token = os.environ['TWILIO_APIKEY']
        client = TwilioRestClient(account, token)

        toNumber = _parseNumber(phoneNumber)
        fromNumber = _parseNumber(os.environ['TWILIO_NUMBER'])

        sent = client.messages.create(to=toNumber, 
                                      from_=fromNumber,
                                      body=message)

    def _zmqEndpoint(self, contactData, title, message):
        ctx = zmq.Context()
        sock = ctx.socket(zmq.PAIR)
        sock.connect(self.FUNC_TEST_ENDPOINT)
        sock.send(json.dumps({'contactData': contactData,
                              'title': title,
                              'message': message}))
        sock.close()

    def _emailEndpoint(self, email, subject, body):
        """
        Sends an email with the given parameters.
        """
        # Prepare the message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'donotreply@' + self.APP_DOMAIN
        msg['To'] = email

        # Send it
        try:
            smtp = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
            smtp.login(self.SMTP_LOGIN, self.SMTP_PASSWORD)
            smtp.sendmail(msg['From'], msg['To'], msg.as_string())
            smtp.quit()
        except smtplib.SMTPException:
            print "Error: unable to send email"  #Eric

    def _gmailEndpoint(self, email, subject, body):
        """
        Sends an email from gmail with the given parameters.
        This is mainly used for local testing.
        """
        # gmail credentials
        gmail_user = os.environ['GMAIL_TEST_USER']
        gmail_pwd = os.environ['GMAIL_TEST_PW']
        # Prepare actual message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = email

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.close()
            print "Notification successfully sent"
        except Exception as e:
            print e
            print "Notification failed to send"

    @staticmethod
    def generateAckURL(uuid, user):
        """
        Given the Event UUID and the user, generate the Ack URL
        """
        ack_append = '/API/ackEvent/?uuid={uuid}&apiKey={apiKey}'
        ack_url = APP_URL + ack_append.format(uuid=uuid, apiKey=user.apiKey)

        return ack_url

    @staticmethod
    def shortenURL(url):
        """
        Given a URL, shorten it with bitly
        """
        import bitly_api
        #Hack to make bit.ly work
        long_url = url
        if 'localhost' in long_url:
            long_url = long_url.replace('localhost', 'lvh.me')

        bitlyUser = os.environ['BITLY_USER']
        bitlyApikey = os.environ['BITLY_APIKEY']
        c = bitly_api.Connection(bitlyUser, bitlyApikey)
        return c.shorten(long_url)['url']

    @staticmethod
    def appendAckInfo(uuid, user, message, shorten_url=False):
        """
        Creates the Ack URL and appends ack information to the given message.

        Args:
            uuid (str):         event UUID
            user (UserPCM):     user to address the ack to
            message (str):      message to append after
            shorten_url (bool): whether or not to shorten the URL
        """
        ack_url = PageSender.generateAckURL(uuid, user)
        if shorten_url:
            ack_url = PageSender.shortenURL(ack_url)
        msg = message + '\nAck URL: ' + ack_url
        return msg
