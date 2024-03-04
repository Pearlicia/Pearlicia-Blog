# Set up email server on EC2

## Prerequisites

1. **Domain:** You should have a registered domain

2. Contact AWS to open port 25 it is blocked by default

    **Port 25:** When using the SMTP protocol to transfer or exchange email over the internet, port 25 is the default port.

    **Reason ISP's block port 25:** The only practical way for Internet service providers to stop virus writers from using a compromised computer to send out thousands, if not millions, of spam emails is to block the port.


## Steps:

### Step 1:
Create and launch an Ubuntu instance with minimum 8gb storage

- A volume of 30Gb storage is attached here
- Create inbound rule and add all this ports

    1. HTTP	TCP	80	0.0.0.0/0	

    2. All TCP	TCP	0 - 65535	0.0.0.0/0	

    3. DNS (TCP)	TCP	53	0.0.0.0/0	

    4. POP3	TCP	110	0.0.0.0/0

    5. SMTPS	TCP	465	0.0.0.0/0	

    6. SMTP	TCP	25	0.0.0.0/0	

    7. MSSQL	TCP	1433	0.0.0.0/0	

    8. IMAPS	TCP	993	0.0.0.0/0	

    9. DNS (UDP)	UDP	53	0.0.0.0/0	

    10. SSH	TCP	22	0.0.0.0/0	

    11. HTTPS	TCP	443	0.0.0.0/0	

    12. IMAP	TCP	143	0.0.0.0/0	

    13. POP3S	TCP	995	0.0.0.0/0	

### Step 2: 
Create and associate an elastic IP to the new instance

Use this [link](https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a13.36.12.139&run=toolpage) to check if the elastic IP is blacklisted or not

### Step 3:
- Create a subdomain called mail.yebox.net
- Copy the NS values then create an NS record in yebox.net and paste the values
- Create another record on yebox.net this time create an A record, copy the mail server elastic IP and paste in the value field 

### Step 4:
Go to Elastic IP dashboard, click on the elastic IP name then click `actions` then click on `update reverse DNS` enter the subdomain `mail.yebox.io` and update

### Step 5:
Go the subdomain and create an MX record: Leave name field blank, type `10 mail.yebox.net` on the value field 

### Step 6:
Connect to your instance
- type `sudo hostname mail.yebox.net`
- The `hostname`
- Then install **Docker**
- Install git

### Step 7:
The mail cow doc [link](https://docs.mailcow.email/getstarted/install/#docker)
- cd /opt
- sudo git clone https://github.com/mailcow/mailcow-dockerized
- cd mailcow-dockerized
Run `sudo ./generate_config.sh`
- enter `mail.yebox.net` on hostname
- leave timezone as default
- Choose version 1 which is the latest version

### Step 8: 
Run `sudo docker compose pull`
Then `sudo docker compose up -d`

### Step 9: Change Admin password
- Open `https://mail.yebox.net` on a browser
- Login using `admin` as username and `moohoo` as password
Click on `system` then `configuration` then `Edit` to change admin password

### Step 10: Add a domain and finish DNS setup
- Click on `E-Mail` dropdown then select `configuration`
- Click `Add domain` button then fill the form
    - On `domain` type `yebox.net`
    When done click `add domain and restart SOGo`
    On the created domain page click on the `DNS` button on the far right

### Step 11: Add DKIM, SPF and DMARC for security and authentication
After doing this **On the created domain page click on the `DNS` button on the far right**
Create record for all the available DNS on the page(Ones that are not created already)

If every record has been created successfully, email receiving should work fine but not sending because port 25 is still blocked. Create a mailbox and send an email from gmail to the newly created mailbox.


### Step 12: To send email using Amazon SES

If AWS refuses to open port 25 for sending email an alternative way to achieve this is to use Amazon Simple Email Service

- Have the domain verified on SES
- To create your SMTP credentials
    Sign in to the AWS Management Console and open the Amazon SES console at https://console.aws.amazon.com/ses/.

    Choose `SMTP settings` in the left navigation pane - this will open the Simple Mail Transfer Protocol (SMTP) settings page.

    Choose Create SMTP Credentials in the upper-right corner - the IAM console will open.

    (Optional) If you need to view, edit, or delete SMTP users you’ve already created, choose Manage my existing SMTP credentials in the lower-right corner - the IAM console will open. Details for managing SMTP credentials is given following these procedures.

    For Create User for SMTP, type a name for your SMTP user in the User Name field. Alternatively, you can use the default value that is provided in this field. When you finish, choose Create user in the bottom-right corner.

    Select Show under SMTP password - your SMTP credentials are shown on the screen.

    Download these credentials by choosing Download .csv file or copy them and store them in a safe place, because you can't view or save your credentials after you close this dialog box.

    Choose Return to SES console.

### Step 13:

Docs on how to add relay host on mailcow [link](https://docs.mailcow.email/manual-guides/Postfix/u_e-postfix-relayhost/)

On mailcow UI 
- Cliick on `E-Mail`
- Then `configuration`
- Then `Routing`

Add **Sender-dependent transports**
Get host and port on SES by clicking `SMTP settings`
- On `Host` type `email-smtp.eu-west-3.amazonaws.com:587`
- On `username` add SMTP username
- On `password` add SMPT password

After saving it. Go to the domain and edit it to include the newly added `Sender-dependent transports` from the dropdown. Save after edit. Then email sending should be possible.



