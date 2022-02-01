import json
import boto3
import urllib.request


pinpoint = boto3.client('pinpoint')

def get_conditions(spot_id):
        url = "http://services.surfline.com/kbyg/spots/forecasts/conditions?days=1&spotId=" + spot_id 
        user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
        headers = {"User-Agent": user_agent}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        raw = response.read()
        forecasts = json.loads(raw)
    
        observation = forecasts["data"]["conditions"][0]["observation"]
        
        am_avg = (int(forecasts["data"]["conditions"][0]["am"]["maxHeight"]) + 
                 int(forecasts["data"]["conditions"][0]["am"]["minHeight"])) / 2
        am_rat = forecasts["data"]["conditions"][0]["am"]["rating"]
        
        pm_avg = (int(forecasts["data"]["conditions"][0]["pm"]["maxHeight"]) + 
                 int(forecasts["data"]["conditions"][0]["pm"]["minHeight"])) / 2
        pm_rat = forecasts["data"]["conditions"][0]["pm"]["rating"]
        
        return f"Condition is going to be AM {am_rat} {am_avg}ft and PM: {pm_rat} {pm_avg}ft.\n\n{observation}"


def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    number = message['originationNumber']
    user_input = message['messageBody']
    
    d = {"1": "5842041f4e65fad6a7708827" ,"2": "5842041f4e65fad6a770888a", "3": "5842041f4e65fad6a7708828", "4": "584204214e65fad6a7709b9f", "5": "584204204e65fad6a7709435"}
    if user_input in d.keys(): 
        bot_output = get_conditions(d[user_input])
    else:
        bot_output = (
        "Hi, I can help to show you the current surf conditions."
        "Which point would you want to know?\n"
        "Reply:\n"
        "1: Huntington\n"
        "2: Trestles\n"
        "3: Ventura\n"
        "4: Malibu\n"
        "5: Oceanside\n"
        )
        


    pinpoint.send_messages(
        ApplicationId='5d8e6b921524489cb0205f5f68cc9691',
        MessageRequest={
            'Addresses': {
                number : {'ChannelType': 'SMS'}
            },
            'MessageConfiguration': {
                'SMSMessage': {
                    'Body': bot_output,
                    'MessageType': 'PROMOTIONAL'
                }
            }
        }
    )
    
    