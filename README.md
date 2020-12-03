# QAPracticalProject

## Links
- [Jira Board](https://iwanmoreton.atlassian.net/jira/software/projects/RPG/boards/2) 
- [Risk Assessment](https://docs.google.com/spreadsheets/d/1IeuFpi1XlGLEOQXmaGHo8kVIGX8WgU8-X_HEDSg3zGQ/edit?usp=sharing)
- [Website]()

## Contents
- [Brief](#brief)
    - [Requirements](#requirements)
    - [My Approach](#my-approach)
- [CI Pipeline](#ci-pipeline)
- [Tracking](#tracking)
- [Version Control](#version-control)
- [Risk Assessment](#risk-assessment)
- [Testing](#testing)
    

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

## CI Pipeline

### Initial Pipeline
![Imgur](https://i.imgur.com/zBeTDPh.png)
The initial pipeline used for the application was a single branch pipeline following the diagram above. The pipeline was controlled using Jenkins with 3 stages defined in the Jenkinsfile (Test, Build, Deploy). The test stage would use a Python virtual environment to run Pytest unit tests to test the responses given from the APIs. Once the tests had passed the VM Jenkins is installed on would build the images using ` docker-compose build `and push them to Docker Hub using ` docker-compose push `, I chose DockerHub as it was, in my opinion, more portable than other options as the only configuration needed was for the docker hub user to be logged in or the image to be public. The deploy stage would then ssh into the Docker Swarm manager, pull the project repository from GitHub, pull the images and then use ` docker stack deploy --compose-file docker-compose.yaml` to deploy the application accross the swarm. Deployment was automated through the use of a GitHub webhook that triggered on each push and merge to the main branch. The problem with this initial pipeline was that it required the swarm manager and the workers to be manually set up. Thie meant that the deployment of this pipeline was not portable as it required a lot of configuration to deploy. 
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
The second implementation of the pipeline was very similar to the first except was made into a multibranch pipeline, using the BlueOcean plugin from Jenkins. The BlueOcean plugin allows for multibranch pipelines using the original Jenkinsfile, with the use of an access token produced by GitHub to allow it to access repositories linked to my GitHub account. The webhook was then updated to trigger on all events, this allowed Jenkins to run the pipeline on every branch of the repository, on each push. As this meant the application was deployed on every push to every branch, there were problems introduced if the updates stopped the application working as intended. To fix this, I added the below code to each stage of the pipeline that should only be ran on the main branch. 
'''groovy 
  when {
    branch 'main'  
  }
'''


## Tracking
I used [Jira](https://iwanmoreton.atlassian.net/jira/software/projects/RPG/boards/2) to track the progress of the project.
![Imgur](https://i.imgur.com/eatK3Hp.png)
I used epics to keep track of each part of the application, this included each service. testing and containerisation. This allowed me to check the backlog for sub issues of each epic and assign these to sprints, this then allowed me to use a board for the sprint that would keep track of which issues hadn't been started, which were in progress and which were completed for the sprint.

IMAGE OF BOARD HERE

Jira also produces charts and reports automatically for the sprints. On a larger project these would be a lot more informative but, as sprints for this project were only a few hours at a time, the reports produced weren't as informative but still produced a visual of how long issues took to complete based on story points(where i remembered to add them). Below is an example of a burnup report
![Imgur](https://i.imgur.com/TNEIb6t.png)
In the future I think it would be a better idea to integrate Jira with my VCS, to automatically keep track of issues as I found that I became distracted and forgot to move them across.

## Version Control
For this project I used Git as version control with GitHub as the provider. I used a feature-branch system throughout with very few commits to main. This allowed me to keep track of the feature I was focussing on and would have allowed for me to roll back on features if a particular merge broke the application. I also made use of a .gitignore file to make sure that unnecessary files, such as pycache files, were omitted from each commit.
![Imgur](https://i.imgur.com/ubj78kC.png)
## Risk Assessment
I made use of a risk assessment for this project, which can be found [here](https://docs.google.com/spreadsheets/d/1IeuFpi1XlGLEOQXmaGHo8kVIGX8WgU8-X_HEDSg3zGQ/edit?usp=sharing). 
![Imgur](https://i.imgur.com/3c1eDOA.png)
## Testing
I used pytest to test the application. These tests were designed to check that the output of each service was in the correct format for service 2 and 3. 

For service 4 I used mock testing to mock the return of the API used for name generation and then unit tested the result to check that the results were as expected. 

Service 1 also required mock patch testing with the requests_mock library to patch get requests from both service 2 and 3. I also used unittests built in patch function to patch the return from service 4. The data returned from service 1 is then checked to make sure it contains the information it would have recieved from services 2,3, and 4.

Below is the coverage report, showing the high percentage of coverage achieved, with the only lines not tested being the app runners.
![Imgur](https://i.imgur.com/Gney1rL.png)
