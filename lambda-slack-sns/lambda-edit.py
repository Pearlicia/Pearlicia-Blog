import boto3
import json
import logging
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ssm = boto3.client("ssm")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print(json.dumps(event))

    message = json.loads(event['Records'][0]['Sns']['Message'])
    print(json.dumps(message))

    alarm_name = message['AlarmName']
    #old_state = message['OldStateValue']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']

    slack_message = {
        'text': " :fire: %s state is now %s: %s" % (alarm_name, new_state, reason)
    }

    webhook_url = ssm.get_parameter(
        Name = 'SlackWebhookURL', WithDecryption=True
    )

    req = Request(webhook_url['Parameter']['Value'],
            json.dumps(slack_message).encode('utf-8')
    )

    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
