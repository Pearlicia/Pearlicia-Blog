To achieve your goal, you can modify your existing Lambda function to retrieve the CloudWatch logs associated with the provided HTTP link and then parse through those logs to find the specific error message. Here's how you can approach this:

Retrieve Logs from CloudWatch: Extract the log group name and log stream name from the provided HTTP link. Use the boto3 library to fetch the CloudWatch logs associated with these names.

Parse Logs for Error Message: Iterate through the log events retrieved from CloudWatch logs and search for the error message using regex or simple string matching.

Handle Error Message: If the error message is found, take appropriate actions, such as sending a notification or logging the message for further analysis.

Send Notification to Slack: Once the error message is found, you can send a notification to Slack containing relevant information, including the error message, pipeline name, status, etc.

Here's a high-level overview of how you can update your Lambda function:




Certainly! Below is the completed code with additional logic for parsing CloudWatch logs, extracting relevant information, and sending a notification to Slack:

```python
import boto3
import json
import re
import urllib3

def lambda_handler(event, context):
    # Extract the HTTP link from the event
    http_link = event['http_link']
    
    # Parse the HTTP link to extract log group name and log stream name
    parsed_link = urllib.parse.urlparse(http_link)
    log_group_name = parsed_link.path.split('/')[1]
    log_stream_name = parsed_link.path.split('/')[3]

    # Initialize CloudWatch Logs client
    logs_client = boto3.client('logs')
    
    # Retrieve the CloudWatch logs
    response = logs_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name
    )
    
    # Initialize variables to store error messages and other relevant information
    error_messages = []
    pipeline_name = ""
    status = ""
    source = ""
    # Add more variables as needed
    
    # Parse through log events to find error messages and extract other information
    for event in response['events']:
        message = event['message']
        # Example: Search for 'ERROR' in the log message
        if 'ERROR' in message:
            error_messages.append(message)
        # Extract other information like pipeline name, status, etc.
        # Example: Extract pipeline name from the log message
        if 'PipelineName' in message:
            pipeline_name = re.search(r'PipelineName: (.+)', message).group(1)
        if 'Status' in message:
            status = re.search(r'Status: (.+)', message).group(1)
        if 'Source' in message:
            source = re.search(r'Source: (.+)', message).group(1)
        # Add more parsing logic as needed
    
    # Construct the message to send to Slack
    slack_message = {
        'text': f'Error messages found in {pipeline_name} pipeline:\n{", ".join(error_messages)}\n'
                f'Pipeline name: {pipeline_name}\n'
                f'Status: {status}\n'
                f'Source: {source}'
        # Add more information to the message as needed
    }
    
    # Send the message to Slack
    # Assuming you have a Slack webhook URL defined in your environment variables
    webhook_url = os.environ['SLACK_WEBHOOK_URL']
    http = urllib3.PoolManager()
    response = http.request("POST", webhook_url, body=json.dumps(slack_message), headers={'Content-Type': 'application/json'})
    
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent to Slack!')
    }
```

Make sure to replace `'SLACK_WEBHOOK_URL'` with the actual name of your environment variable containing the Slack webhook URL. Also, ensure that your Lambda function's execution role has permission to access CloudWatch logs and send HTTP requests to the specified Slack webhook URL.