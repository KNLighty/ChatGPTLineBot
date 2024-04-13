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
        # URL for the LINE Messaging API
        url = 'https://api.line.me/v2/bot/message/reply'

        # Generate response
        response = generate_response(message_event['message']['text'])
        
        
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
                    "text": response
                }
            ]
        }
        
        # Creating a request object with necessary parameters
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
        
        # Opening the URL and sending the request, capturing the response
        with urllib.request.urlopen(req) as res:
            # Logging the response content (Assuming logger is defined elsewhere)
            logger.info(res.read().decode("utf-8"))
            

    # Returning a response indicating successful executio
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

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
