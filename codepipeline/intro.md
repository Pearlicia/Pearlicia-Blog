# What is Codepipeline
Code pipeline is a fully managed service for continuous delivery and integration that assists you in automating release pipelines for dependable and quick updates to your infrastructure and applications. 

Among AWS's developer tools, code pipeline serves as the intermediary and processor for various AWS services. It pulls in source code and initiates a pipeline execution via code commit or an alternative external source control system. Code build is used for building software, running code, and pretty much any other task you have in your pipeline. It will typically turn out to be among the most crucial steps in your cicd procedure. Lambda functions can be triggered to run at any point in your pipeline, which increases the possibilities of what you can accomplish with that pipeline. And lastly, a variety of deployment services, including codeDeploy, elastic beanstalk, ECS, and fargate, are compatible with code pipeline. Code Pipeline's numerous integrations guarantee that you can complete any scenario you need to.

## Comparing Codepipeline to orther CICD tools like Jenkins, TravisCI, CircleCI
- Circle CI, Jenkins, and Travis CI are similar to code pipeline in that they offer automated continuous integration and continuos delivery services. 
- Workflow definition is used by Jenkins, TravisCI, Codepipeline, and CircleCI. A file and a workflow can be defined, and the workflow will start when it receives a trigger—typically, a change to source control. 
- Unlike Codepipeline, which only uses AWS, Circle CI, Jenkins, and Travis CI aren't dependent on any one cloud provider or even any cloud provider at all, so they can operate with or without AWS. 
- Through the robust and flexible AWS API, circleCI and travisCI can interact with resources in aws, but it would have to be manually configured and written. 
- In addition code pipeline only costs one dollar per pipeline excluding any processing time with codebuild or storage in s3.

## Codepipeline's Internal Features

The term "pipeline" refers to each unique instance of codepipeline. It includes all of the pipeline's configuration options, as well as a minimum of two to a maximum of ten stages, and within those stages, one to fifty actions. Soon, we will delve deeper into each of these topics. With the use of input and output artifacts—which are simply files—a pipeline can transport a certain kind of state between each action and stage, such as your input source code, pipeline status files, or a build application binary. Code pipeline stores its artefacts in an S3 bucket, which serves as the primary means of interaction between your actions. Each action defines its own unique identifier name, and if you need to input an artefact that was output from a previous action, you simply need to reference it by the name as an input artefact, and Code Pipeline will retrieve it from the pipeline S3 bucket. 

## Pipeline Configuration Options
- **Pipeline Name Identifier:** In order to be identified, pipelines only need to have a unique name within the same account region.
- **Service Role with Access to most AWS Services:** A service role is required for a pipeline in order to grant it access to lambda, s3, code commit, and the numerous other resources that code pipeline uses.
- **S3 Bucket to act as the Artifact Store:** To store the input and output artefacts used and produced by the pipeline, an S3 bucket must be created or assigned. 
- **Encryption Key: Yours in KMS or default Amazon-provided** Lastly, you have the option to use the default AWS encryption key or assign your own kms encryption key for the artefacts in the S3 bucket. 

A pipeline only has a number of stages in addition to these configuration options.

## Anatomy of a Stage
A pipeline can have up to ten stages, but as I previously stated, it must have at least {two stages}. A stage is essentially just a group of actions that you can use to group and separate various action kinds based on any criteria you choose. The simplest illustration is to have a:

- **Source Stage:** Which contains an action that pulls code from source control and generate an output that contains the source code artifact. 
- **Build Stage:** which includes a few actions that run build commands on that source code artefact. 
The only true requirement is that the first stage `must contain one or more source actions and nothing more`. Other than that, you are free to use stages to structure your pipeline however you see fit. Additionally, in my experience, I've found that the pipeline's transitions between stages do introduce a small amount of latency; not a lot, but enough that I've started using stages extremely sparingly.

### Actions in a Stage
There is a minimum of `one action` and a `maximum of 50 actions` permitted in each stage. The magic of a pipeline happens in an action. Every action has a specific purpose and comes in a few different varieties. 

### Action Types in Code Pipeline
- **Source Action Type:** This particular action type, which pulls source code from one of the providers—such as Github, Bitbucket, Gitlab, Codecommit, ECR, or S3 can only be seen in the first stage.
 
- **Build Type:** These actions run a job on one of the build providers that are available, such as Codebuild or Jenkins. This is usually where the code for your application is built or compiled. If necessary, you can also instruct a codebuild job to execute arbitrary code. For instance, you could instruct it to execute commands via the AWS CLI. 

- **Test Action Type:** Automated testing is a crucial component of automated deployment, and the test action type helps you incorporate it into your pipeline. There are many different providers for the test action type including various third parties like Ghost Inspector, Runscope, BlazeMeter, Device Farm CodeBuild and Jenkins. And also just using codebuild to run your tests. 

- **Deploy Action Type:** Deploying your code is usually something you'll want to do near the end of your pipeline, and the deploy action type can help you with that. For deploying your application, there are numerous options available, including well-known AWS services like CodeDeploy, ECS, Elastic Beanstalk, S3, and Cloudformation. 

**There are two more action types you may find useful the first is the:** 

- **Approval Action Type:** Which enables you to add a manual approval to your pipeline. This is very useful if you have a pipeline that deploys to production and you would like someone to manually test a new version before it is actually deployed.

- **Invoke Action Type:** which enables you to call a lambda function later on in your workflow.

## Pipeline Creation
Let's take a look at how to create a pipeline. You can do this by running a template in cloud formation or by navigating through a wizard on the AWS console. I strongly advise using cloudformation for the creation of your pipeline since I'm a big believer in maintaining control over your infrastructure and sources. Another reason cloudformation is better is that I frequently find myself needing to use cloudformation to create pipelines that are similar but for different applications and regions. With just a few minor template modifications, a completely new pipeline can be set up and operational in a matter of minutes. We'll build pipelines in both directions in this tutorial so you can see when to use each method.
