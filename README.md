# Lazzaro Infrasturcture Deployment


## Architecture frontend deployment
![aws-devops](https://personal-website-assets.s3.amazonaws.com/Projects/Lazzaro/frontend_deployment_architecture_add_service.jpeg)


### Functions
client: frontend-ecs-services-pre-client
createservice: frontend-ecs-services-pre-createservice
removeservice: frontend-ecs-services-pre-removeservice
testservice: frontend-ecs-services-pre-testservice
deletesecuritygroup: frontend-ecs-services-pre-deletesecuritygroup

### Mechanism to deploy infrasturcture in different environments
```
sls deploy --stage (pre/prod)
sls deploy --f (function_name) --stage (pre/prod)
```