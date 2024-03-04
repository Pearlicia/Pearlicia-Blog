# Real-time Monitoring of 5XX Errors using AWS Lambda, CloudWatch Logs and Slack

## Prerequisites:

- A CloudWatch agent must be configured on your server to send logs to CloudWatch Logs.
- An incoming webhook for the Slack channel of your choice. You can make one by following this [guide](https://slack.com/help/articles/115005265063-Incoming-webhooks-for-Slack). An incoming webhook is basically an endpoint to a Slack channel. In order to send alert messages to a channel, we simply have to send a POST request to its webhook.


1. The CloudWatch agent installed on the EC2 instance sends log events to CloudWatch Logs.

2. We’ll set up a subscription filter to filter out 5xx events. A subscription filter is a CloudWatch Logs feature that allows sending of real-time feeds of log events to other AWS services such as AWS Lambda, Amazon OpenSearch Service, Amazon Kinesis Data Stream, and Amazon Kinesis Data Firehose. In our case, we’ll use AWS Lambda.

3. Filtered events are sent to a Lambda function. The Lambda function parses the event data, formats it to a Slack message, and sends it to a channel via a webhook.