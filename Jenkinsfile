pipeline {
  agent any
  environment {
    registry = "tmapp"
    awsRegion = 'us-west-2'
    awsECR = '287171483464.dkr.ecr.us-west-2.amazonaws.com'
    awsEKSCluster = 'tm-app'
  }
  stages {
    stage('Test/Lint') {
      steps {
        sh 'docker run --rm -i hadolint/hadolint < Dockerfile'
      }
    }
    stage('Build Docker Image') {
      steps {
            sh "docker build -t ${awsECR}/${registry} ."
            sh "docker tag ${awsECR}/${registry} ${awsECR}/${registry}:${GIT_COMMIT}"
      }
    }
    stage('Obtain AWS Credentials') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-static	', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
        sh '''
               mkdir -p ~/.aws
               echo "[default]" >~/.aws/credentials
               echo "[default]" >~/.boto
               echo "aws_access_key_id = ${AWS_ACCESS_KEY_ID}" >>~/.boto
               echo "aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}">>~/.boto
               echo "aws_access_key_id = ${AWS_ACCESS_KEY_ID}" >>~/.aws/credentials
               echo "aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}">>~/.aws/credentials
               aws eks --region ${awsRegion} update-kubeconfig --name ${awsEKSCluster}
        '''
        }
      }
    }
    stage('Upload Docker Image') {
      steps {
            sh "docker push ${awsECR}/${registry}:${GIT_COMMIT}"
      }
    }
    stage('Identify Live') {
        steps {
            script {
                def currentEnvironment = 'blue'
                def newEnvironment = { ->
                    currentEnvironment == 'blue' ? 'green' : 'blue'
                }

                currentEnvironment = sh (
                    script: 'kubectl get services tmapp-service --output json | jq -r .spec.selector.role',
                    returnStdout: true
                ).trim()
                
                echo "***************************  CURRENT: ${currentEnvironment}     NEW: ${newEnvironment()}  *****************************"

                env.TARGET_ROLE = newEnvironment()
                targetEnvironment = newEnvironment()
                
                sh 'kubectl delete deployment tmapp-\$TARGET_ROLE'
            }
        }
    }
    stage('Deploy Standby') {
        steps {
            script {
                sh "cp deployment.template.yml deployment.${GIT_COMMIT}.yml"
                sh "sed -i -e 's|%targetEnvironment%|${targetEnvironment}|g' deployment.${GIT_COMMIT}.yml"
                sh "sed -i -e 's|%targetImage%|${awsECR}/${registry}:${GIT_COMMIT}|g' deployment.${GIT_COMMIT}.yml"
                sh "kubectl apply -f deployment.${GIT_COMMIT}.yml"
            }
        }
    }
    stage('Switch Approval') {
        input{
		    message "Press Ok to continue"
	    }
	    steps { 
		    echo "Approved."
	    }
    }
    stage('Switch Live') {
      steps {
            script {
                sh "cp service.template.yml service.${GIT_COMMIT}.yml"
                sh "sed -i -e 's|%targetEnvironment%|${targetEnvironment}|g' service.${GIT_COMMIT}.yml"
                sh "kubectl apply -f service.${GIT_COMMIT}.yml"
            }
        }
      
    }
  }
}