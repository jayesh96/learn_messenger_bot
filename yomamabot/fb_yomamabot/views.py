# yomamabot/fb_yomamabot/views.py
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAACRFYZByztkBACN6HZBh36huXK9gYBoUAonX1wOW0nEQSthJwyXntaxRAsaFeEtiVLjaxs7asbLaEkvgNPUTMaGFgsoSjIxwmrk2d422AwmLirZBmG0X2W7ugwHxwJ3SWWVIjdsdeabznyCfC170emnv33Ob6fgfZCIRBmUxAZDZD"
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
      "type": "image",
      "payload": {
      	"url": "http://combiboilersleeds.com/images/sun/sun-8.jpg",
        "is_reusable": true
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
