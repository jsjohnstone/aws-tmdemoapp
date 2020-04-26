# AWS Exploration Projects
## Deploy a docker container to a kubernetes cluster

The goal of this project was to learn about setting up a Kubernetes cluster, and deploying a Docker container to the cluster using a blue/green deployment strategy.

### What does the app do?
The demonstration app is a simple Python flask application that obtains the Top 20 events for sale through Ticketmaster. As it's just a proof of concept to work with while learning about kubernetes clusters and docker containers, it's simple and doesn't handle exceptions.

### How does the deployment pipeline work?
The package includes a Jenkinsfile which defines the following pipeline:

#### 1. Test/List
This step does simple linting of the dockerfile to ensure it has been written correctly, using *hadolint*.

#### 2. Build Docker Image
This step builds a new docker image using the source obtained from Git and tags it with the git commit hash.

#### 3. Obtain AWS Credentials
This is a simple step that brings the necessary credentials into the environment to enable Jenkins to (a) upload the docker image to ECR and (b) obtain the necessary configuration to manage the kubernetes cluster.

#### 4. Upload Docker Image
This step uploads the tagged docker image to Amazon ECR.

#### 5. Identify Live
The kubernetes cluster is setup with two deployments: blue and green. The service for this application points at one deployment/pod at a time (e.g. blue), allowing new versions of the app to be staged on the other deployment/pod (e.g. green). This step queries kubernetes to identify which deployment/pod is currently live: blue or green.

#### 6. Deploy Standby
Using the identified live deployment above (e.g. blue), this step deploys the new docker image to the other environment (e.g. green).

#### 7. Approval
This step pauses the deployment pipeline until approval is received, allowing the developer to check the new image has deploymed correctly in the other environment (e.g. green).

#### 8. Switch Live
Finally, this step directs the app service to point to the new environment (e.g. green), making the new version of the app 'live'.

## Kubernetes Cluster Structure
The kubernetes cluster contains:
1 x Load Balancer (tmapp-service)
2 x Deployments (tmapp-blue and tmapp-green)

The load balancer points at one of the deployments, allowing new versions of the application to be deployed to the other deployment, and once approved, for the load balancer to be switched to this new version.
