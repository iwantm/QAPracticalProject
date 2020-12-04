# QAPracticalProject

## Links
- [Jira Board](https://iwanmoreton.atlassian.net/jira/software/projects/RPG/boards/2) 
- [Risk Assessment](https://docs.google.com/spreadsheets/d/1IeuFpi1XlGLEOQXmaGHo8kVIGX8WgU8-X_HEDSg3zGQ/edit?usp=sharing)
- [Website](http://34.105.241.249/)

## Contents
- [Brief](#brief)
  - [Requirements](#requirements)
  - [My Approach](#my-approach)
- [Risk Assessment](#risk-assessment)
- [Tracking](#tracking)
- [Version Control](#version-control)
- [Architechture](#architechture)
  - [ERD](#erd)
  - [Infrastrcuture](#infrastrcuture)
- [CI Pipeline](#ci-pipeline)
  - [Initial Pipeline](#initial-pipeline)
  - [Second Implementation](#second-implementation)
  - [Third Implementation](#third-implementation)
  - [Fourth Implementation](#fourth-implementation)
  - [Benefits of Pipeline](#benefits-of-pipeline)
  - [Branch views](#branch-views)
  - [Logging](#logging)
- [Pipeline Stages](#pipeline-stages)
  - [Test](#test)
  - [Build](#build)
  - [Setup](#setup)
  - [Deployment](#deployment)
- [Changes](#changes)
  - [Service 1](#service-1)
  - [Risk Assessment](#risk-assessment)


    

## Brief
### Requirements
The requirements the project had to meet were:
- An Asana board (or equivalent Kanban board tech) with full expansion on tasks needed to complete the project.
- An Application fully integrated using the Feature-Branch model into a Version Control System which will subsequently be built through a CI server and deployed to a cloud-based virtual machine.
- If a change is made to a code base, then Webhooks should be used so that Jenkins recreates and redeploys the changed application
- The project must follow the Service-oriented architecture that has been asked for.
  - Service #1: The core service – this will render the Jinja2 templates you need to interact with your application, it will also be responsible for communicating with the other 3 services, and finally for persisting some data in an SQL database.
  - Service #2 + #3 - These will both generate a random “Object”, this object can be whatever you like as we encourage creativity in this project.
  - Service #4 - This service will also create an “Object” however this “Object” must be based upon the results of service #2 + #3 using some pre-defined rules.
- The project must be deployed using containerisation and an orchestration tool.
- As part of the project, you need to create an Ansible Playbook that will provision the environment that your application needs to run.
- The project must make use of a reverse proxy to make your application accessible to the user.

### My Approach
To meet the given requirements, I decided to create an application that will randomly generate a person. Service 2 is used to generate the country of birth and corresponding from a dictionary, service 3 is used to to select the gender of the person and service 4 is used to generate the name using the outputs from services 2 and 3. Service 4 is a POST request driven API that takes the language spoken(given by service 2) and the gender(given by service 3). It then uses the [Behind the name API](https://www.behindthename.com/api/) to generate a name based on the language and gender, this is then returned as JSON in the POST response. Service 1 is used to perform the GET requests on services 2 and 3, and the POST request on service 4. It then takes the response from service 4 and uses HTML and Jinja2 templating to return this to the user, as well as the country of birth and gender. Service 1 also provides a button for the user to press to generate a new person.The application uses Docker containerisation to deploy the services across a Docker swarm of 4 machines(3 workers and one manager) all hosted using GCP. This is then deployed using a Jenkins multi-branch pipeline.

This provides a worker per service, this could be added to at a later date to cope with increased traffic if necessary. Each service has 4 replicas as this allows each machine to run every service of the application, this should allow for machines to be removed or updated with little-to-no downtime.

## Risk Assessment
I made use of a risk assessment for this project, which can be found [here](https://docs.google.com/spreadsheets/d/1IeuFpi1XlGLEOQXmaGHo8kVIGX8WgU8-X_HEDSg3zGQ/edit?usp=sharing). 
![Imgur](https://i.imgur.com/3c1eDOA.png)

## Tracking
I used [Jira](https://iwanmoreton.atlassian.net/jira/software/projects/RPG/boards/2) to track the progress of the project.
![Imgur](https://i.imgur.com/eatK3Hp.png)
I used epics to keep track of each part of the application, this included each service. testing, containerisation and Jenkins. This allowed me to check the backlog for sub issues of each epic and assign these to sprints, this then allowed me to use a board for the sprint that would keep track of which issues hadn't been started, which were in progress and which were completed for the sprint.

![Imgur](https://i.imgur.com/jNvwR65.png)

Jira also produces charts and reports automatically for the sprints. On a larger project these would be a lot more informative but, as sprints for this project were only a few hours at a time, the reports produced weren't as informative but still produced a visual of how long issues took to complete based on story points(where i remembered to add them). Below is an example of a burnup report

![Imgur](https://i.imgur.com/TNEIb6t.png)

In the future I think it would be a better idea to integrate Jira with my VCS, to automatically keep track of issues as I found that I became distracted and forgot to move them across. Jira has good GitHub integration, so this should be easy enough in the future.

## Version Control
For this project I used Git for version control with GitHub as the provider. I made use of a feature-branch system, with the only commits to main being merges and hotfixes for smaller issues. This allowed me to focus on features of the application and merge these in as necessary. Once the pipeline was introduced to the project, this also allowed me to see if the changes had passed the unit testing before I merged them to main to be automatically deployed. This allowed for me to roll back the application easily if a merge had caused issues with the application. I also made use of a .gitignore file to make sure that unnecessary files weren't included in the repo.

![Imgur](https://i.imgur.com/ubj78kC.png)

## Architechture
### ERD
As the database only stores the generated names and genders, it only requires one table for persisting data. 
![Imgur](https://i.imgur.com/4ZsXN1P.png)

### Infrastrcuture
The Jenkins server and Ansible were run on the dame machine, as it means that less configuration is needed, with only the public key from the Jenkins server being needed when creating the other machines. This isn't much of a problem as Ansible doesn't require much power to be used. This also means that it is more cost effective as it doesn't require an extra VM. The swarm consists of a manager and 3 workers, which are configured by Ansible dependant on the role set. NGINX was used as a load balancer and was set up by Ansible as well.
![Imgur](https://i.imgur.com/vY6WYHM.png)

## CI Pipeline
### Initial Pipeline
![Imgur](https://i.imgur.com/zBeTDPh.png)
The initial pipeline I used for the application was a single branch pipeline. The pipeline was controlled by Jenkins with 3 stages defined in the Jenkinsfile (Test, Build, Deploy). The test stage used a Python virtual environment to run unit tests on each of the services. Once the tests had finished running the server would then build and push the images to Docker Hub. I chose Docker Hub as I believe it to be more portable than other options available as it doesnt require extra configuration to pull the images and only requires a log in to push the images. The deploy stage would then SSH into the swarm manager, pull the project respository from GitHub, pull the images using the docker-compose file and then deploy the application to the swarm. Deployment was automated through a web hook which was triggered on each push to the main branch. The main problem with this initial pipeline was that it required the swarm manager and workers to be set up manually. This meant that the pipeline was not portable as it required a large amount of configuraion to be deployed across the swarm.

```groovy 
  pipeline {
  agent any
  stages {
    stage('Testing') {
      steps {
        sh './scripts/test.sh'
      }
    }

    stage('Build') {
      when {
        branch 'main'
            }
      steps {
        sh './scripts/build-images.sh'
      }
    }

    stage('Deploy App') {
      when {
        branch 'main'
            }
      steps {
        sh './scripts/deploy.sh'
      }
    }

  }
}
```
### Second Implementation
![Imgur](https://i.imgur.com/6Zn0Duj.png)

The second implementation of the pipeline used the same base Jenkinsfile as the first, with few changes. The main difference between this implementation and the first was the introduction of the BlueOcean Jenkins Plugin that allowed for a multibranch pipeline to be set up. The BlueOcean plugin requires a GitHub access token to your account, so that it can check your repositories. It then lets you pick which repository you want to run a CI/CD server for, and searches it for a Jenkinsfile. The last change was to make the webhook trigger on all events, so that BlueOcean knows when a push is made to any branch. The Jenkinsfile had to be updated for the Build and Deploy steps with the below code so that it wasnt building and deploying on all branches, as this would have led to downtime as any errors in any branch would be automatically deployed.
```groovy 
  when {
    branch 'main'  
  }
```
### Third Implementation
![Imgur](https://i.imgur.com/JaGoT0t.png)
The third implementation of the pipeline fixed the main issue found with the first implementation, with the introduction of a configuration step using Ansible to automatically install and configure the Docker Swarm. The added step removes the need to manually configure each swarm machine, instead just needing to add either the name or private IP to the Ansible inventory. The problem with this was a lack of notifications when builds had passed or failed.
```groovy 
  stage('Setup'){
      when{
        branch "main"
      }
      steps{
        sh './scripts/ansible.sh'
      }
    }
```
### Fourth Implementation
The fourth and current implementation of the pipeline had the exact same stages as the third(Test, Build, Setup, Deploy). Although added Telegram notifcations on each stage of the build, with the testing stage sending a message if it had passed or failed, the Build and Setup stages only sending messages on failure, and the deployment stage sending a message if the build had successfully deployed or not. The messages were sent using the Telegram http bot API and curl. The lines below show which lines were added to testing to achieve this, with the format being similar for the other stages:
```groovy 
  environment {
    TELEGRAM_BOT = credentials('telegram_bot')
  }
  stages {
    stage('Testing') {
      steps {
          sh './scripts/test.sh'
      }
    post{
      success {
        script{
          sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\\&text=' + BRANCH_NAME + '%20passed%20tests'
        }
      }
      failure {
        sh 'curl https://api.telegram.org/bot'+ TELEGRAM_BOT +'/sendMessage?chat_id=539893428\\&text=' + BRANCH_NAME + '%20failed%20tests'
      }
    }
  }
```
![Imgur](https://i.imgur.com/fPwJnw4.png)
This is an example of the messages sent by the bot.

### Benefits of Pipeline
The multibranch pipeline allowed for benefits during the latter development of the project. As each branch ran the unit testing of the application, this meant that I was given message notifcations when tests had passed. This also allowed GitHub to tell me if a branch can be merged based on if it had passed tests.
![Imgur](https://i.imgur.com/GhwkmGJ.png)
This would allow me to choose whether to merge pull requests based on successful tests rather than risking the deployment of the application.
### Branch views
The BlueOcean plugin for Jenkins also much improved the user interface for Jenkins, which made it easier to see which stage the pipeline was in. This meant that accessing the logs produced for builds was much easier and it was all in one place.
![Imgur](https://i.imgur.com/Y776tZv.png)
It also showed the stages being skipped for the other branches.
![Imgur](https://i.imgur.com/Sd7g1tw.png)
### Logging
After each step Jenkins produces logs on both successful builds and failed builds. These are accessable using the Jenkins UI and are able to be opened as plain text in a seperate window.
![Imgur](https://i.imgur.com/DZjBd9n.png)

![Imgur](https://i.imgur.com/3Eu9OZj.png)



## Pipeline Stages
These stages are triggered on every push of the main branch. All of the other branches and pull requests, only go through the test stage.
### Test
I used pytest to test the application. These tests were designed to check that the output of each service was in the correct format for service 2 and 3. 

For service 4 I used mock testing to mock the return of the API used for name generation and then unit tested the result to check that the results were as expected. 

Service 1 also required mock patch testing with the requests_mock library to patch get requests from both service 2 and 3. I also used unittests built in patch function to patch the return from service 4. The data returned from service 1 is then checked to make sure it contains the information it would have recieved from services 2,3, and 4.

Below is the coverage report, showing the high percentage of coverage achieved, with the only lines not tested being the app runners.
![Imgur](https://i.imgur.com/Gney1rL.png)

To run this in the pipeline I created a script that would create a venv and install the dependencies for testing, it would then run pytest on each test file to make sure it passes. Once complete the script deleted the virtual environment.

### Build
The build step of the pipeline builds the images for Docker. It uses the docker-compose tool to build the images based on the docker-compose.yaml using the command `docker-compose build `. It builds the images based on the Dockerfile for each service and then pushes each image to a repository on DockerHub using the image name provided in the compose file. 

### Setup
The setup stage of the pipeline uses Ansible to initialise the Docker Swarm, using SSH to access each machine. The roles provided for the swarm are common, worker and manager with the common role installing Docker and docker-compose with the dependencies required. The manager role initialises the swarm and stores the token as a host variable. The worker role uses the join token to join the swarm as a worker. This allows the swarm to be used for the deployment of the application in the next step. 

### Deployment
The last step of the pipeline that deploys the application to the swarm. This stage of the pipeline uses SSH to connect to the swarm manager and pull the docker images from DockerHub using the compose file. Docker stack is then used to deploy the services across the nodes using the images pulled earlier in the step.



## Changes
### Service 1 
In intial development of service 1 I was using a if else statement for the gender name on the page.
```python
    if gender["gender"] == 'f':
        gender_name = 'female'
    else:
        gender_name = 'male'
```
This caused issues as it meant that if the return from service 3 was incorrect it would just default as male.
I updated this to be more correct by changing it from an else statement to a elif statement, making sure that it was checking correctly.
```python
    if gender["gender"] == 'f':
        gender_name = 'female'
    elif gender["gender"] == 'm':
        gender_name = 'male'
```
### Risk Assessment
During development of the application it was found that some errors in the code were not picked up by unit testing. One of these errors was the database connection timing out. In turn I added a section for errors not being picked up by testing to my risk assessment.
![Imgur](https://i.imgur.com/Sib0cZW.png)


## Author
Iwan Moreton


