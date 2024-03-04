import json
import urllib3
import logging
import boto3
import random
from urllib.parse import unquote
import re

# Define your GIPHY GIF URLs
GIPHY_GIF_URLS = [
    "https://media.giphy.com/media/3o85xs8qEtiqFPjrUc/giphy.gif",
    "https://media.giphy.com/media/eiFQZdejnerUkvHFeJ/giphy.gif",
    "https://media.giphy.com/media/l41Ym49ppcDP6iY3C/giphy.gif",
    # Add more GIF URLs here
]

def lambda_handler(event, context):
    # Initialize urllib3 for making HTTP requests
    http = urllib3.PoolManager()
    
    # Replace 'your_slack_webhook_url_here' with your actual Slack webhook URL
    webhook_url = "your_slack_webhook_url_here"
    
    # Select a random GIF URL
    gif_url = random.choice(GIPHY_GIF_URLS)
    
    # Set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        # Read message posted on SNS Topic
        event_breakdown = json.loads(event["Records"][0]["Sns"]["Message"])
        logger.info("Message: " + str(event_breakdown))
        
        # Extract relevant information from the message
        status = event_breakdown["detail"]["build-status"]
        pipeline_name = event_breakdown["detail"]["additional-information"]["initiator"]
        deeplink = event_breakdown["detail"]["additional-information"]["logs"]["deep-link"]
        source = event_breakdown["detail"]["additional-information"]["source"]
        
        # Extract error messages from the message
        error_messages = []
        for phase in event_breakdown["detail"]["additional-information"]["phases"]:
            phase_context = phase.get("phase-context")
            if phase_context and "ERROR:" in phase_context[0]:
                error_messages.append(phase_context[0])
        error_messages_str = "\n".join(error_messages)
        logger.info("Error: " + str(error_messages))
        
        # Decode the log group name
        decoded_deeplink = unquote(deeplink)
        log_group_name_decoded = decoded_deeplink.split("/log-group/")[1].split("/log-events")[0]
        log_stream_name = deeplink.split("/log-events/")[1]
        logger.info("Decoded Log Group Name:" + str(log_group_name_decoded))
        logger.info("Log Stream Name:" + str(log_stream_name))
        
        # Use the log group and stream information to retrieve error files from CloudWatch Logs
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
            
            for event in log_events['events']:
                message = event['message']
                timestamp = event['timestamp']
                logger.info(message)
                
                # Process each log event
                failed_tests_match = re.search(r"Failed tests: (.+)", message)
                if failed_tests_match:
                    failed_tests_line = failed_tests_match.group(1)
                    print(f"Failed tests: {failed_tests_line}")
                
                tests_in_error_match = re.search(r"Tests in error: (.+)", message)
                if tests_in_error_match:
                    tests_in_error_line = tests_in_error_match.group(1)
                    print(f"Tests in error: {tests_in_error_line}")
                
                tests_run_match = re.search(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)", message)
                if tests_run_match:
                    tests_run, failures, errors, skipped = map(int, tests_run_match.groups())
                    if failures > 0 or errors > 0:
                        tests_run_line = f"Tests run: {tests_run}, Failures: {failures}, Errors: {errors}, Skipped: {skipped}"
                        print(tests_run_line)
            
            if next_token is None:
                break
        
        # Prepare data for Slack message
        pipeline_info = "*Pipeline name:* %s\n*Status:* %s\n*Source:* %s" % (pipeline_name, status, source)
        failed_messages = "*Results:* %s\n👋 *Revisit:* %s" % (tests_run_line, error_messages_str)
        
        data = {
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": "@channel"}},
                {"type": "header", "text": {"type": "plain_text", "text": ":rotating_light:*CODEBUILD FAILURE INFORMATION*:rotating_light:"}},
                {"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn", "text": pipeline_info},
                 "accessory": {"type": "image", "image_url": gif_url, "alt_text": "memes"}},
                {"type": "divider"},
                {"type": "section", "block_id": "section568", "text": {"type": "mrkdwn", "text": "*Cause of Failure:* %s" % error_messages_str}},
                {"type": "section", "text": {"type": "mrkdwn", "text": failed_messages}},
                {"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn", "text": "View original logs here--->"},
                 "accessory": {"type": "button", "text": {"type": "plain_text", "text": "Click Me"}, "value": "click_me_123", "url": deeplink, "action_id": "button-action"}}
            ]
        }
        
        # Send message to Slack
        response = http.request("POST", webhook_url, body=json.dumps(data), headers={"Content-Type": "application/json"})
        print("Message sent to Slack")
        
        return {"statusCode": 200, "body": json.dumps("Notification sent to Slack!")}
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return {"statusCode": 500, "body": json.dumps("An error occurred!")}


Corrected the indentation to ensure consistency.
Added comments to explain the purpose of each section of code.
Moved the assignment of webhook_url to a position where it's properly initialized. Replace "your_slack_webhook_url_here" with your actual Slack webhook URL.
Removed unnecessary print statements.
Used logging.error() instead of print() for error logging.
Wrapped the main code block in a try-except block to catch and log any exceptions.
Added a return statement in the except block to return an error response.



