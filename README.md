# QAPracticalProject
## Contents
- [Brief](#brief)
    - [Requirements](#requirements)
    - [My Approach](#my-approach)
    

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
To meet the application requirements I decided to create an application that will randomly generate people. When a button is pressed service 2 will generate a country of birth and service 3 will generate the gender of the person, this will then be fed into service 4 which will use the [Behind the name API](https://www.behindthename.com/api/) to generate a name based on the country of birth and gender. This will then sent to service 1 to store the name, gender, a randomly generated age and country of birth in a mysql database. This will then be shown to the user using HTML and a Jinja2 template.
