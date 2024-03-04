import json
import urllib3
import logging
import boto3
import random
from urllib.parse import unquote
import re


GIPHY_GIF_URLS = [
"https://media.giphy.com/media/3o85xs8qEtiqFPjrUc/giphy.gif",
"https://media.giphy.com/media/eiFQZdejnerUkvHFeJ/giphy.gif",
"https://media.giphy.com/media/l41Ym49ppcDP6iY3C/giphy.gif",
"https://media.giphy.com/media/D7knpKzFbgDPBmdrVM/giphy.gif",
"https://media.giphy.com/media/zQPoPn1iFrIcM/giphy.gif",
"https://media.giphy.com/media/P4E2rQCDh25Bhiudrh/giphy.gif",
"https://media.giphy.com/media/2zdnl4CB3OygOHe1kX/giphy.gif",
"https://media.giphy.com/media/KEvFx5M4E0VrIVFGYO/giphy.gif",
"https://media.giphy.com/media/yhBiZRplGgwByWBf9v/giphy.gif",
"https://media.giphy.com/media/nR4L10XlJcSeQ/giphy.gif",
"https://media.giphy.com/media/nR4L10XlJcSeQ/giphy.gif",
"https://media.giphy.com/media/mfOQOkAqvWdUsYSvjW/giphy.gif",
"https://media.giphy.com/media/dJGYFScvBjfRabiH7m/giphy.gif",
"https://media.giphy.com/media/loNqveG4p6J7Gszeyk/giphy.gif",
"https://media.giphy.com/media/sHhZiG2mU7ZBjmPGI3/giphy.gif",
"https://media.giphy.com/media/1xVbRS6j52YSzp9P7N/giphy.gif",
"https://media.giphy.com/media/M9mRamx5xdUe1fjHSr/giphy.gif",
"https://media.giphy.com/media/jEc3j5MkMq9vlXZGgq/giphy.gif",
"https://media.giphy.com/media/J4jW3l7R4mQkABSAXp/giphy.gif",
"https://media.giphy.com/media/Heqbbp1m3mzJe/giphy.gif",
"https://media.giphy.com/media/pWdckHaBKYGZHKbxs6/giphy.gif"
]


def lambda_handler(event, context):
#used to make http requests, great for its added features and performance
http = urllib3.PoolManager()
#Our copia slack webhook leading to build_notification channel
webhook_url =
gif_url = random.choice(GIPHY_GIF_URLS)

#logs incoming info to Cloudwatch for easy troubleshooting
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Read message posted on SNS Topic
event_breakdown = event["Records"][0]["Sns"]["Message"]
message = json.loads(event_breakdown)
logger.info("Message: " + str(message))


# Extract the build status and project name
status = message["detail"]["build-status"]
pipeline_name = message["detail"]["additional-information"]["initiator"]
deeplink = message["detail"]["additional-information"]["logs"]["deep-link"]
source = message["detail"]["additional-information"]["source"]


# Extract error messages from the message
error_messages = []
for phase in message["detail"]["additional-information"]["phases"]:
phase_context = phase.get("phase-context")
if phase_context and "ERROR:" in phase_context[0]:
error_messages.append(phase_context[0])

error_messages_str = "\n".join(error_messages)
logger.info("Error: " + str(error_messages))


# Decode the log group name
results_message = []
tests_run_line = ""
try:
# Decode the log group information
decoded_deeplink = re.sub(r'%([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), deeplink)
log_group_name_base = unquote(deeplink)
log_group_name_changed = log_group_name_base.replace("$252F", "/")
log_group_name_decoded = log_group_name_changed.split("/log-group/")[1].split("/log-events")[0]
log_stream_name = deeplink.split("/log-events/")[1]
logger.info("Decoded Log Group Name:" + str(log_group_name_decoded))
logger.info("Log Stream Name:" + str(log_stream_name))



# Use new information to retrieve error files
client = boto3.client('logs')
start_time = 0
next_token = None



while True:
if next_token:
log_events = client.get_log_events(
logGroupName=log_group_name_decoded,
logStreamName=log_stream_name,
nextToken=next_token,
startTime=start_time
)
else:
log_events = client.get_log_events(
logGroupName=log_group_name_decoded,
logStreamName=log_stream_name,
startTime=start_time
)


# Process each log event
for event in log_events['events']:
message = event['message']
timestamp = event['timestamp']
logger.info(message)



failed_tests_match = re.search(r"Failed tests: (.+)", message)
if failed_tests_match:
failed_tests_line = failed_tests_match.group(1)
print(f"Failed tests: {failed_tests_line}")
results_message.append(f"Failed tests: {failed_tests_line}\n")



tests_in_error_match = re.search(r"Tests in error: (.+)", message)
if tests_in_error_match:
tests_in_error_line = tests_in_error_match.group(1)
print(f"Tests in error: {tests_in_error_line}")
results_message.append(f"Tests in error: {tests_in_error_line}\n")



# Check if the number of Failures or Errors is greater than 0 in the "Tests run" section
tests_run_match = re.search(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)", message)
if tests_run_match:
tests_run, failures, errors, skipped = map(int, tests_run_match.groups())
if failures > 0 or errors > 0:
tests_run_line = f"Tests run: {tests_run}, Failures: {failures}, Errors: {errors}, Skipped: {skipped}"
print(tests_run_line)



if message == "Tests in error:" or message == "Failed tests:":
tests_record = True
tests_in_error_count = 0 # Reset counter for each section
elif tests_record:
tests_in_error_match = re.search(r" (\S+)(?=\:)", message)
if tests_in_error_match:
tests_in_error_list.append(tests_in_error_match.group(1))
tests_in_error_count += 1
else:
# Check for "Tests run:" line and failures/errors
tests_run_match = re.search(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)", message)
if tests_run_match:
failures = int(tests_run_match.group(2))
errors = int(tests_run_match.group(3))
if failures + errors > 0:
other_ending_condition = tests_in_error_count >= failures + errors
if other_ending_condition:
tests_record = False
else:
other_ending_condition = tests_in_error_count > 5
if other_ending_condition:
tests_in_error_started = False
print(tests_in_error_list)



next_token = log_events.get('nextForwardToken', None)
start_time = log_events['events'][-1]['timestamp'] + 1 if log_events['events'] else 0



if next_token is None:
break
break
except Exception as e:
logger.error(f"An error occurred: {str(e)}")
results_message = "Check the logs for more details"
print(results_message)



print("sending message to slack now")
pipeline_info = "*Pipeline name:* %s\n*Status:* %s\n*Source:* %s" % (pipeline_name, status, source)
print(pipeline_info)
failed_messages = "*Results---->* %s\n👋*Revisit:*:small_red_triangle_down: %s" % (tests_run_line, results_message)
print(failed_messages)
# Add a random GIF to the message
print("Starting to build slack message in acceptable format")
data = {
"blocks": [
{
"type": "section",
"text": {
"type": "mrkdwn",
"text": "@channel"
}
},
{
"type": "header",
"text": {
"type": "plain_text",
"text": ":rotating_light:*CODEBUILD FAILURE INFORMATION*:rotating_light:"
}
},
{
"type": "divider"
},
{
"type": "section",
"text": {
"type": "mrkdwn",
"text": pipeline_info
},
"accessory": {
"type": "image",
"image_url": gif_url,
"alt_text": "memes"
}
},
{
"type": "divider"
},
{
"type": "section",
"block_id": "section568",
"text": {
"type": "mrkdwn",
"text": "*Cause of Failure: %s*" % error_messages
}
},
{
"type": "section",
"text": {
"type": "mrkdwn",
"text": failed_messages
}
},
{
"type": "divider"
},
{
"type": "section",
"text": {
"type": "mrkdwn",
"text": "View original logs here--->"
},
"accessory": {
"type": "button",
"text": {
"type": "plain_text",
"text": "Click Me"
},
"value": "click_me_123",
"url": deeplink ,
"action_id": "button-action"
}
}
]
}
print("data created for slack and ready to send... sending")
response = http.request("POST",
webhook_url,
body = json.dumps(data),
headers = {"Content-Type": "application/json"})
print("Message sent to slack")



return {
"statusCode": 200,
"body": json.dumps("Notification sent to Slack!")
}

