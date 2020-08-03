from flask import Flask, request, make_response
import requests
import os
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    auth_header = os.getenv('NETILION_AUTH')
    api_key = os.getenv('NETILION_API_KEY')
    req = request.get_json(silent=true, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    if intent == 'GetOverview':
        request_headers = {'accept': 'application/json', 'Authorization': auth_header, 'Api-Key': api_key}
        get_total_assets_result = requests.get('https://api.netilion.endress.com/v1/assets', headers=request_headers)
        get_total_assets_json = get_total_assets_result.json()
        count_total_assets = get_total_assets_json['pagination']['total_count']

        get_failure_assets_result = requests.get('https://api.netilion.endress.com/v1/assets?status_code=failure*', headers=request_headers)
        get_failure_assets_json = get_total_assets_result.json()
        count_failure_assets = get_total_assets_json['pagination']['total_count']

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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')