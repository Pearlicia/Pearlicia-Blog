# Send SNS to Slack via Lambda

## Step 1: Slack Webhook
- Create new slack workspace
- Then go to this [url](https://api.slack.com/apps?new_app=1)
- Click on create new app 
- Click from scratch
- On `App Name` Choose a name e.g `notifications`
- On `Pick a workspace to develop your app in` Select your newly created workspace
- Then click `Create App`
- On the next page click on `Incoming webhooks` under **Features**
- Click on the `Activate Incoming Webhooks` button to turn it on 
- Click on `Add New Webhook to Workspace` button at the bottom of the page
- Select the channel you want to post to then click on the `Allow` button
- Copy the `Webhook url` shown on the next page https://hooks.slack.com/services/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

## Step 2: System Manager Parameter Store
To save the Webhook url in System manager parameter store
- Create a parameter store with `SlackWebhookURL` as the name
- Choose `Secure string` under **Type**
- On `Value` enter your webhook url
- Then click on `Create parameter`

## Step 3: EC2 And Cloudwatch
- Create an EC2 instance
- Then search for `Cloudwatch` click on `Alarms`
- Click on `In alarm` then click on the `Create alarm` button
- Click on `Select metric` button
- Click on `EC2` then click on `Per-Instance Metric`
- Copy and paste the EC2 instance ID on the search bar
- Then tick `CPUUtilization` then click `Create metric`
- On `Threshold type` Leave it as `Static`
- On `Whenever CPUUtilization is...` select `Greater` enter 10 on `Than` you can enter any value depending on your requirement
- Then click `next`
- Select `Create a new topic` choose a name for the topic
- Enter an email address on the next field
- Click on `Create topic` Then click on `Next` button
- Enter Alarm name then click `Next`
- Scroll down and click on `Create alarm`

## Step 4: Create Role
First create a policy called `kms-policy-for-decryption`
- Go to IAM click on `Policies`
- Click on `Create policy` button
- Click on `JSON`
- Open another tab and search for `kms` click on `Key management service`
- Click on `AWS managed keys` on the left panel
- Click on `aws/ssm` and copy the ARN, paste it on the resource part
- The policy should look like this
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Action": [
			    "kms:Decrypt"
			 ],
			"Resource": [
			    "arn:aws:kms:us-east-1:113782462018:key/3a717fd0-d23b-447a-8fc9-a6199952a649"
			]
		}
	]
}

```
- Click `Next` and enter the policy name e.g `kms-policy-for-decryption`
- Click on `Create policy`

- Go to IAM 
- Click on `roles` then click on `Create role`
- Select `AWS service`
- On `Service or use case` select **Lambda** then click `Next`
- 1. On permission page search for `AWSLambdaBasicExecutionRole` and select it
- 2. Also search for `AmazonSSMFullAccess` and select it
- 3. On `Filter by type` select `Customer managed` Search for the newly created policy(kms-policy-for-decryption) if it does not appear click on `Refresh policies` and select it

## Step 5: Lambda
- Search for lambda service and click on it
- Click on the `Create function` button
- Select `Author from scratch`
- On `Function name` enter your function name e.g cloudwatch-sns-slack
- On `Runtime` choose python3.any number
- On `Architecture` select **x86_64**
- On `Execution role` select **Use an existing role**
- Select the name of the role created above refresh if it does'nt appear 
- Click on `Create function`

## Step 6: Integrate Lambda with SNS
- On the lambda function page click on the `Add trigger` button
- On `select a source` select `SNS`
- On `SNS topic` select the SNS topic you created while configuring cloudwatch
- Click on the `Add` button