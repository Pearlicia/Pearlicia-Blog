I currently have a python script running on lambda on AWS that is pinged when my code pipeline fails. My payload from the ping provides me with a http link (link to failed pipeline logs). The goal is to create a scrip that parses through the cloudwatch logs (a ton of them) and finds a certain error message (there are keywords the pipeline logs when an error occurs) from it that will help me figure out what went wrong.

1. Python script
2. Script running on lambda
3. Runs or triggers when codepipeline fails
4. Payload from the ping provides http link(link to failed pipeline logs)

**Goal**
1. Create a script that parses through cloudwatch logs(a ton of them) and find a certain error message from it that will help figure out what went wrong(There are keywords the pipeline logs when an error occurs)

# Step 1: Python script running on lambda

**Note:** Ensure that your Lambda function has the necessary IAM permissions to access CloudWatch logs.

To achieve your goal, you can modify your existing Lambda function to retrieve the CloudWatch logs associated with the provided HTTP link and then parse through those logs to find the specific error message. Here's how you can approach this:

- **Retrieve Logs from CloudWatch:** Extract the log group name and log stream name from the provided HTTP link. Use the boto3 library to fetch the CloudWatch logs associated with these names.

- **Parse Logs for Error Message:** Iterate through the log events retrieved from CloudWatch logs and search for the error message using regex or simple string matching.

- **Handle Error Message:** If the error message is found, take appropriate actions, such as sending a notification or logging the message for further analysis.

- **Send Notification to Slack:** Once the error message is found, you can send a notification to Slack containing relevant information, including the error message, pipeline name, status, etc.