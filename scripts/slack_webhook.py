import requests 
import json 
import os 


def post_via_webhook(payload: str):
    url = os.environ["SLACK_WEBHOOK_URL"]
    # Create a slack incoming webhook. At the "app management" page, you'll see the webhook URL. It looks something like "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX". Add to your environment variable.

    response = requests.post(
        url, 
        data=json.dumps({"text": payload}),
        headers={'Content-type': 'application/json'}
    )
    return response.status_code, response.text


if __name__ == "__main__":
    print(post_via_webhook("Test send message to Slack."))