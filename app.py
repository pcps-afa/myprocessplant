from flask import Flask, request, make_response
import requests
import os
import json
import urllib.parse

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    auth_header = os.getenv('NETILION_AUTH')
    api_key = os.getenv('NETILION_API_KEY')
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    if intent == 'GetOverview':
        request_headers = {'accept': 'application/json', 'Authorization': auth_header, 'Api-Key': api_key}
        get_total_assets_result = requests.get('https://api.netilion.endress.com/v1/assets', headers=request_headers)
        get_total_assets_json = get_total_assets_result.json()
        count_total_assets = get_total_assets_json['pagination']['total_count']

        get_failure_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=failure*', headers=request_headers)
        get_failure_assets_json = get_failure_assets_result.json()
        count_failure_assets = get_failure_assets_json['pagination']['total_count']

        answer = 'There are currently ' + str(count_total_assets) + ' connected assets. ' + str(count_failure_assets) + ' is currently in failure status'

        return make_response({
            "fulfillmentText": answer,
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses":{
                        "simpleResponses": [
                            {
                                "textToSpeech": answer
                            }
                        ]
                    }
                }
            ],
            "source": "webhook"
        })
    elif intent == 'ForwardFirstFailureStatusCauseAndRemedy':
        get_failure_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=failure*', headers=request_headers)
        get_failure_assets_json = get_failure_assets_result.json()
        asset_id = get_failure_assets_json['assets'][0]['id']

        get_cause_remedy_url = 'https://api.netilion.endress.com/v1/assets/' + str(asset_id) + '/health_conditions?include=causes%2C%20causes.remedies'
        get_cause_remedy_result = requests.get(get_cause_remedy_url, headers=request_headers)
        get_cause_remedy_json = get_cause_remedy_result.json()
        diagnosis_code = get_cause_remedy_json['health_conditions'][0]['diagnosis_code']
        cause = get_cause_remedy_json['health_conditions'][0]['causes'][0]['description']
        remedy = get_cause_remedy_json['health_conditions'][0]['causes'][0]['remedies'][0]['description']

        get_asset_location_url = 'https://api.netilion.endress.com/v1/assets/' + str(asset_id) + '/nodes'
        get_asset_location_result = requests.get(get_asset_location_url, headers=request_headers)
        get_asset_location_json = get_asset_location_result.json()
        location = get_asset_location_json['nodes'][0]['name']

        answer = 'An asset in location ' + location + ' reads diagnostic code ' + diagnosis_code + '. The cause is: ' + cause + '. The recommendation is: ' +remedy
        
        telegram_auth = os.getenv('TELEGRAM_AUTH')
        telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        telegram_request_url = 'https://api.telegram.org/bot' + telegram_auth + '/sendMessage?chat_id=-' + telegram_chat_id + '&text=' + urllib.parse.quote(answer)
        telegram_response = requests.get(telegram_request_url)

        if telegram_response.status_code == 200:
            return make_response({
                "fulfillmentText": "message was sent out",
                "fulfillmentMessages": [
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "simpleResponses":{
                            "simpleResponses": [
                                {
                                    "textToSpeech": "message was sent out"
                                }
                            ]
                        }
                    }
                ],
                "source": "webhook"
            })
        else:
            return make_response({
                "fulfillmentText": "message could not be sent",
                "fulfillmentMessages": [
                    {
                        "platform": "ACTIONS_ON_GOOGLE",
                        "simpleResponses":{
                            "simpleResponses": [
                                {
                                    "textToSpeech": "message could not be sent"
                                }
                            ]
                        }
                    }
                ],
                "source": "webhook"
            })




if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')