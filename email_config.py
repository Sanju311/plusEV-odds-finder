from simplegmail import Gmail


SENDER_EMAIL = "evbetfinder99@gmail.com"
SENDER_PASSWORD = "Evbetfinder55"
RECEIVER_EMAILS = "sanjumoorthy622@gmail.com"

#run application with the command: --noauth_local_webserver
#for when browser is on a different machine


def sendMail(event, bet, odds, EV, experimental):

    
    try: 
        gmail = Gmail()

        event_info = event['outcomes'][0] +' vs ' + event['outcomes'][1] + " in the " + event['leauge']
        eventTime = "commencing on: " + event['start_time']
        
        params = {
            "to": RECEIVER_EMAILS,
            "sender": SENDER_EMAIL,
            "subject": "FOUND A BET",
            "msg_html": "<h1>" +event_info + "<br><br>" + eventTime + "<br><br>" + bet +" has a price of: " + str(odds) + "<br><br> and has an EV of: " + str(EV) + "<br><br>" + experimental + "</h1>",
            "signature": True
        }
        
        print("Sending Email...")
        message = gmail.send_message(**params)
        print("Email Sent!")
    
    except Exception as e:
        print("could not send email")
        print(e)

