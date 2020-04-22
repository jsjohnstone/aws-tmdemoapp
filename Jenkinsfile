pipeline {
  agent any
  environment {
    registry = "jsjohnstone/tmapp"
    registryCredential = 'dockerhub'
  }
  stages {
    stage('Test/Lint') {
      steps {
        sh "echo 'Test/Lint'"
      }
    }
    stage('Build Docker Image') {
      steps {
            sh "docker build -t ${registry}:latest ."
      }
    }
    stage('Upload Docker Image') {
      steps {
        withDockerRegistry([ credentialsId: registryCredential, url: "" ]) {
            sh "docker push ${registry}:latest"
        }
      }
    }
    stage('Obtain AWS Credentials') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-static	', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
        sh """  
               mkdir -p ~/.aws
               echo "[default]" >~/.aws/credentials
               echo "[default]" >~/.boto
               echo "aws_access_key_id = ${AWS_ACCESS_KEY_ID}" >>~/.boto
               echo "aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}">>~/.boto
               echo "aws_access_key_id = ${AWS_ACCESS_KEY_ID}" >>~/.aws/credentials
               echo "aws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}">>~/.aws/credentials
        """
        }
      }
    }
    stage('Create EC2 Instance') {
      steps {
        sh "echo 'Create'"
      }
    }
  }
}