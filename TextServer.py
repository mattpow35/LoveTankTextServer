from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import redis
from twilio.rest import Client

app = Flask(__name__)

redis_host = "localhost"
redis_port = 6379
msg = ""

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
my_twilio_num = '+18609796457'
admin_num = "+18019604992"

try:
    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)



except Exception as e:
    print(e)


def getPartnerNum(fnum):
    return r.get(fnum + ":partner_num")


def getPartnerName(fnum):
    return r.get(fnum + ":partner_name")


def getPartnerLoveLang1(fnum):
    return r.get(getPartnerNum(fnum) + ":love_lang_1")


def getPartnerLoveLang2(fnum):
    return r.get(getPartnerNum(fnum) + ":love_lang_2")


def getCurrUserName(fnum):
    return r.get(fnum + ":name")

def triggerReminders():
    numbers = r.lrange("phone_numbers", 0, -1)
    i = 0
    for num in numbers:
        print(getCurrUserName(num))
        if num is not None:
            i += 1
            client.messages \
                .create(
                body="Hey " + getCurrUserName(num) + ", what is your love tank at today?\n\nRespond with a number 1-10, but not 7 ;)",
                from_='+18609796457',
                to=num
            )

    return i

def sendMessageToPartner(message, from_num):
    client.messages \
        .create(
        body=message,
        from_='+18609796457',
        to=getPartnerNum(from_num)
    )

def send_GIF_for_7(from_num):
    client.messages \
        .create(
            body="Sorry 7 is not a valid response!",
            media_url="https://media2.giphy.com/media/3ohzdQ1IynzclJldUQ/giphy.gif?cid=ecf05e47y4gmmv803k3ijl4292eavqdh50al1wj0vgm069xr&rid=giphy.gif&ct=g",
            from_='+18609796457',
            to=from_num
    )


@app.route("/initial",methods=['GET'])
def send_initial_message():
    args = request.args
    number = "+"
    number += args['number']
    print(number)
    sendMessageToPartner("Thank you for signing up for Love Tank!", number)

    return("Initial message response.")


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    # get the incoming message
    body = request.values.get('Body', None)

    # get the phone number of incoming message
    from_num = request.values.get("From", None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    message = ""
    loveTankScore = ""
    errorMessage = ""
    isBadResp = False

    if from_num == admin_num:
        if body == "remind":
            num_updates = triggerReminders()
            resp.message("Sent reminders to " + str(num_updates) + " phone numbers")
            return str(resp)


    if body == "1":
        loveTankScore = body
    elif body == "2":
        loveTankScore = body
    elif body == "3":
        loveTankScore = body
    elif body == "4":
        loveTankScore = body
    elif body == "5":
        loveTankScore = body
    elif body == "6":
        loveTankScore = body
    elif body == "7":
        send_GIF_for_7(from_num)
        isBadResp = True
    elif body == "8":
        loveTankScore = body
    elif body == "9":
        loveTankScore = body
    elif body == "10":
        loveTankScore = body
    else:
        isBadResp = True
        errorMessage = "Sorry your response was not recognized, please respond with a single number 1-10 but not 7 ;)"

    if isBadResp:
        message = errorMessage
    else:
        message = "Thank you for updating your Love Tank! :) We will send your response of " + loveTankScore + " to " + getPartnerName(from_num) + "."
        score = int(loveTankScore)
        message_to_partner = "Hi " + getPartnerName(from_num) + ", your significant other " + getCurrUserName(from_num) + \
                             " just updated their Love Tank! Their Love Tank is currently at " + loveTankScore + "."
        if score < 7:
            message_to_partner += "\n\nHere is a reminder of what their love languages are: " +getPartnerLoveLang1(from_num) + \
                " and " + getPartnerLoveLang2(from_num) + ".\n Do something special for them today and fill up their love tank! :)"
        else:
            message_to_partner += "\nGreat Job!"

        sendMessageToPartner(message_to_partner, from_num)

    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4567", debug=True)
