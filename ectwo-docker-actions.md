# Deploying a Node Express server on Amazon EC2 with Docker and GitHub Actions.

We will delve into the topics of automated deployment and containerisation in this guide. Using GitHub Actions, I will walk you through the process of dockerizing a basic node.js application and deploying it to an Amazon EC2 instance. This tutorial can help you optimise your deployment process or introduce you to Docker in a new way.

## What is Docker?

On a high level, Docker is a tool that allows you to package an application and its dependencies into a single image. This image can run on any machine with Docker installed, regardless of the underlying operating system. Docker is a containerization platform, where containers are isolated environments containing everything an application needs to run. Think of Docker as a shipping container for your software application, holding all necessary components like code, libraries, and settings.

### Benefits of Docker:

- **Portability:** Docker images are portable and can run on any machine with Docker installed, simplifying deployment across different environments.
  
- **Reproducibility:** Docker ensures you can create the same environment for your application regardless of the machine it runs on, aiding in debugging and testing.

- **Scalability:** Docker allows horizontal scaling of applications by adding more machines to your cluster.

- **Security:** Docker can be used to create isolated environments, enhancing application security.

## Prerequisites
1. Docker hub account
2. Github account
3. AWS account

## Steps to take
1. Set up project
2. Create dockerfile
3. Add docker hub username and password to github secrets
4. Create an EC2 instance - Use ubuntu image - install docker
5. Create a self hosted runner
6. Write cicd pipeline

## Step 1: Set Up Project
Skip this step if you already have a project to deploy.

If you don't have a project, go to this [Source code](https://github.com/Pearlicia/simple-rest-api) url and download this simple node express application and push to your github

## Step 2: Create Dockerfile

Create a dockerfile in your project if you don't have already.
Here is a simple dockerfile

Dockerfile
```bash
FROM node

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 5000

CMD ["npm","run","start"]
```

## Step 3: Add Docker Hub Username and Password to Github Secrets

1. On your github account: Go to your project repository and click on `Settings`

![settings-button](./assets/github-settings-button.png)

2. On the left panel under `security` click on **`Secrets and variables`**

![secrets-and-variables](./assets/secrets-n-variables.png)

3. Under `Secrets and variables` click on **`Actions`**

![Actions-button](./assets/actions-button.png)

4. Click on the green `New repository secret` button

![new-secret-button](./assets/new-secret.png)

5. On the `Name` field enter **`DOCKER_USERNAME`**
  - On the `Secret` field enter your docker hub username
  - Then click on the green `Add secret` button

![secret-form](./assets/secret-form.png)

6. Repeat step 4 and 5 but this time
  - On the `Name` field enter **`DOCKER_PASSWORD`**
  - On the `Secret` field enter your docker hub password
  - Then click on the green `Add secret` button

## Step 4: Create an EC2 Instance - Use ubuntu image - Install docker

Click this []() link and follow the steps to create an Ubuntu EC2 instance

Click this [Install-docker](./journal/install-docker-on-ec2.md) link and follow the steps to install Docker on your EC2 instance


## Step 5: Create a Self Hosted Runner
### Setting up Self-Hosted Runner on EC2:

Configure a self-hosted runner on AWS EC2 to enable GitHub Actions to run on your instance. The runner will facilitate tasks like pulling the Docker image and running the container.
 
Go to Github repo settings
- Under `Code and automation` tab expand `Actions` and click on `Runners`
- Click on `new self hosted runner` button
- On `Runner image` select `Linux`
- On `Architecture` select `x64`
- Copy the `Download` and `Configure` code step by step and run on the EC2 instance
- when configuring the runner on EC2 terminal it would promt you to enter `runner name` pls enter
  a runner name **don't leave it as default** every other prompt is okay to be left as default
in this guide I set the runner name as `aws-ec2` and the label also as `aws-ec2`


## Step 6: Write CICD Pipeline
In your project root make a directory called `.github` inside the .github directory make 
another directory called `workflows` then inside the workflows directory create
a file you can name it whatever you want but the extension should be a `yml` or `yaml`
Then copy and paste the workflow below

Make the necessary changes to it like on building the image, you can change the image
name to whichever name you prefer. And anywhere you see `pearlicia` change it to your 
github username. On the `deploy` job change the `aws-ec2` to your runner name created in step 5

```bash
name: cicd-docker-ec2

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout source
        uses: actions/checkout@v3
      - name: Login to Docker Hub
        run: docker login -u ${{ secrets.DOCKER_USERNAME }} -p ${{ secrets.DOCKER_PASSWORD }} 
      - name: Build Docker image
        run: docker build -t pearlicia/nodejs-app-cicd-docker-ec2 .

  deploy:
    needs: build
    runs-on: [aws-ec2] # Change the aws-ec2 to your runner name you created in step 5
    steps:
      - name: Pull image from Docker Hub
        run: docker pull pearlicia/nodejs-app-cicd-docker-ec2:latest
      - name: Remove old container (if exists)
        run: docker rm -f nodejs-app-cicd-docker-ec2-container || true
      - name: Run Docker container
        run: docker run -d -p 5000:5000 --name nodejs-app-cicd-docker-ec2-container pearlicia/nodejs-app-cicd-docker-ec2


```

### Workflow Overview:

#### Build Job:

1. **Checkout Source:** Fetch the source code.
2. **Login to Docker Hub:** Authenticate Docker login using GitHub Secrets for Docker username and password.
3. **Build Docker Image:** Build the Docker image for the Node.js application.
4. **Publish Image to Docker Hub:** Push the Docker image to Docker Hub for later use in deployment.

#### Deploy Job:

1. **Pull Image from Docker Hub:** Pull the Docker image from Docker Hub on the EC2 instance.
2. **Delete Old Container:** Remove any existing Docker container to avoid conflicts.
3. **Run Docker Container:** Start the Docker container on the EC2 instance.

**When you're done commit your changes to github to trigger the workflow. If 
both jobs complete then your application has been deployed to EC2

If you get this error 
```bash
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/images/create?fromImage=pearlicia%2Fnodejs-app-cicd-docker-ec2&tag=latest": dial unix /var/run/docker.sock: connect: permission denied
Error: Process completed with exit code 1.
```

Run
```bash
sudo su
```
Then
```bash
chmod 777 /var/run/docker.sock
```

### Accessing the Application:

After deployment, access the Node.js application on the EC2 instance by updating security group inbound rules to allow traffic on port 5000. 

Then copy your public IP to view it in a browser. If you're using this code here
then the url will be http://yourip:5000/api/users

## Conclusion:

Deploying a Node.js application on AWS EC2 using Docker and GitHub Actions streamlines the deployment process, making it more efficient and scalable. Docker's containerization benefits and GitHub Actions automation enhance the overall workflow.

