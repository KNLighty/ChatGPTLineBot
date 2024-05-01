import json
import urllib.request
import os
import openai



# This is the main function that AWS Lambda will invoke when the function is triggered
def lambda_handler(event, context):
    CHATGPT_API_KEY = os.environ.get('CHATGPT_API_KEY')
    openai.api_key = CHATGPT_API_KEY

  # Iterate over each message event in the received payload
    for message_event in json.loads(event['body'])['events']:
        start_loading_animation(message_event['source']['userId'])

        # Generate response
        response = generate_response(message_event['message']['text'])
        
        # Send reply message
        send_reply(message_event, response)
            

    # Returning a response indicating successful execution
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def start_loading_animation(user_id):
    url_loading_animation = 'https://api.line.me/v2/bot/chat/loading/start'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    }
        
    body = {
        "chatId": user_id,
        "loadingSeconds": 5
    }
    
    req = urllib.request.Request(url_loading_animation, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
    with urllib.request.urlopen(req) as res:
        pass

# Generate chatGPT response
def generate_response(text):
    response = openai.Completion.create(
        prompt=text,
        engine='gpt-3.5-turbo-instruct',
        max_tokens=300,
        temperature=0.7,
        n=1,
        stop=None
    )
    if response and response.choices:
        return response.choices[0].text.strip()
    else:
        return "Something seams to be wrong here!"


# Send reply message to a User
def send_reply(message_event, generated_response):
    # URL for the LINE Messaging API
    url = 'https://api.line.me/v2/bot/message/reply'

    # Headers required for the API request
    headers = { 
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    }
        
    # Constructing the message body to be sent as a response
    body = {
        'replyToken': message_event['replyToken'], # Token for replying to the specific event
        'messages': [
            {
                "type": "text",
                "text": generated_response
            }
        ]
    } 

    # Creating a request object with necessary parameters
    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
        
    # Opening the URL and sending the request, capturing the response
    with urllib.request.urlopen(req) as res:
        pass