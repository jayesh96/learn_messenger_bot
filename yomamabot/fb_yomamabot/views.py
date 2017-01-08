# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAACRFYZByztkBAAZC1MqZBq4PqurdHigZB6SB6LeILcxy06ZADtorCQH8lrcZBSvVsOVkUF2ZCumcgQBUHo13r7R1B7HYLFjaT9ZC6HgzrCl6ahKQZBYU0ACW5C1jVsQsQsmJzL3lQlD64OZCxxoEvNwmig3U4yYIGZC0vwBrXvwOo6agZDZD"
VERIFY_TOKEN = "9711377812"

# Helper function
def error_message(fbid, recevied_message):
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    error_text = "Please Enter start to continue"

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":error_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())




def post_facebook_message(fbid, recevied_message):

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    greeting_text = "Hi " + user_details['first_name']+'..! ' + ' Welcome to FoodCham Bot '

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({
  "recipient":{
    "id":fbid,
  },
"message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "airline_boardingpass",
        "intro_message": "You are checked in.",
        "locale": "en_US",
        "boarding_pass": [
          {
            "passenger_name": "SMITH\/NICOLAS",
            "pnr_number": "CG4X7U",
            "travel_class": "business",
            "seat": "74J",
            "auxiliary_fields": [
              {
                "label": "Terminal",
                "value": "T1"
              },
              {
                "label": "Departure",
                "value": "30OCT 19:05"
              }
            ],
            "secondary_fields": [
              {
                "label": "Boarding",
                "value": "18:30"
              },
              {
                "label": "Gate",
                "value": "D57"
              },
              {
                "label": "Seat",
                "value": "74J"
              },
              {
                "label": "Sec.Nr.",
                "value": "003"
              }
            ],
            "logo_image_url": "http://combiboilersleeds.com/images/sun/sun-8.jpg",
            # "header_image_url": "https:\/\/www.example.com\/en\/fb\/header.png",
            # "qr_code": "M1SMITH\/NICOLAS  CG4X7U nawouehgawgnapwi3jfa0wfh",
            # "above_bar_code_image_url": "https:\/\/www.example.com\/en\/PLAT.png",
            "flight_info": {
              "flight_number": "KL0642",
              "departure_airport": {
                "airport_code": "JFK",
                "city": "New York",
                "terminal": "T1",
                "gate": "D57"
              },
              "arrival_airport": {
                "airport_code": "AMS",
                "city": "Amsterdam"
              },
              "flight_schedule": {
                "departure_time": "2016-01-02T19:05",
                "arrival_time": "2016-01-05T17:30"
              }
            }
          },
          {
            "passenger_name": "JONES\/FARBOUND",
            "pnr_number": "CG4X7U",
            "travel_class": "business",
            "seat": "74K",
            "auxiliary_fields": [
              {
                "label": "Terminal",
                "value": "T1"
              },
              {
                "label": "Departure",
                "value": "30OCT 19:05"
              }
            ],
            "secondary_fields": [
              {
                "label": "Boarding",
                "value": "18:30"
              },
              {
                "label": "Gate",
                "value": "D57"
              },
              {
                "label": "Seat",
                "value": "74K"
              },
              {
                "label": "Sec.Nr.",
                "value": "004"
              }
            ],
            "logo_image_url": "http://combiboilersleeds.com/images/sun/sun-8.jpg",
            # "header_image_url": "https:\/\/www.example.com\/en\/fb\/header.png",
            # "qr_code": "M1JONES\/FARBOUND  CG4X7U nawouehgawgnapwi3jfa0wfh",
            # "above_bar_code_image_url": "https:\/\/www.example.com\/en\/PLAT.png",
            "flight_info": {
              "flight_number": "KL0642",
              "departure_airport": {
                "airport_code": "JFK",
                "city": "New York",
                "terminal": "T1",
                "gate": "D57"
              },
              "arrival_airport": {
                "airport_code": "AMS",
                "city": "Amsterdam"
              },
              "flight_schedule": {
                "departure_time": "2016-01-02T19:05",
                "arrival_time": "2016-01-05T17:30"
              }
            }
          }
        ]
      }
    }
  }


  })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Create your views here.
class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)
    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        print(self.request.body.decode('utf-8'))
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    fbid = message['sender']['id']
                    message =  (message['message']['text']).upper()
                    if message == "START" :
                        post_facebook_message(fbid, message)
                    else:
                         error_message(fbid, "Error")

        return HttpResponse()




# {u'message': {u'mid': u'mid.1483788102369:9b03294b75',
#               u'seq': 95395,
#               u'text': u'nice'},
#  u'recipient': {u'id': u'1483348081676134'},
#  u'sender': {u'id': u'1421327557882495'},
#  u'timestamp': 1483788102369}
# {u'message_id': u'mid.1483788109957:e4b43c3418',
#  u'recipient_id': u'1421327557882495'}
