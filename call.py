import requests
import json

import config


def call_to_worker():
    url = "https://calling.api.sinch.com/calling/v1/callouts"
    payload="{\n  \"method\": \"ttsCallout\",\n  \"ttsCallout\": {\n    \"cli\": \"" + config.sinch_phone_from + "\",\n    \"domain\": \"pstn\",\n    \"destination\": {\n      \"type\": \"number\",\n      \"endpoint\": \""+ config.worker_phone +"\"\n    },\n    \"locale\": \"en-US\",\n    \"prompts\": \"#tts[wake up]\"\n  }\n}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic '+ config.sinch_token
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.json())


def get_last_msg_date() -> int:
    response = requests.get(f'https://api.telegram.org/bot{config.tg_api_key}/getUpdates?offset=-1')
    data = response.json()["result"]
    if not data:
        return 0
    if 'message' in data[0]:
        return data[0]['message']['date']
    return 0


def get_last_tweet_date() -> int:
    with open(config.last_tweet_file) as f:
        data = f.read().strip()
    return json.loads(data)['time']

last_update = get_last_msg_date()
last_tweet_date = get_last_tweet_date()
if last_tweet_date > last_update:
    call_to_worker()