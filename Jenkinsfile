pipeline {
  agent any
  environment {
    registry = "tmapp"
    awsRegion = 'us-west-2'
    awsECR = '287171483464.dkr.ecr.us-west-2.amazonaws.com'
    jenkinsAWSCreds = 'aws-static'
    awsEKSCluster = 'tm-app'
    commit = ${GIT_COMMIT[0..7]}
  }
  stages {
    stage('Test/Lint') {
      steps {
        sh 'docker run --rm -i hadolint/hadolint < Dockerfile'
      }
    }
    stage('Build Image') {
      steps {
            sh "docker build -t ${registry}:${commit} ."
            sh "docker tag ${awsECR}/${registry} ${awsECR}/${registry}:${commit}"
      }
    }
    stage('Update kubectl config') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: '${jenkinsAWSCreds}', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
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
    stage('Upload Image') {
      steps {
            sh "docker push ${awsECR}/${registry}:${commit}"
      }
    }
    stage('Identify Live') {
      steps {
        sh "echo 'Identify which zone Service is currently pointing to'"
      }
    }
    stage('Deploy Standby') {
      steps {
        withAWS(region:'us-west-2', credentials:'aws-static') {
            sh '''
            cat <<EOF | kubectl apply -f -
            apiVersion: v1
            kind: ReplicationController
            metadata:
                name: tmapp-blue
                labels:
                    app: tmapp-blue
            spec:
                replicas: 1
                selector:
                    app : tmapp-blue
                template:
                    metadata:
                        labels:
                            app: tmapp-blue
                    spec:
                        containers:
                            - name: tmapp-blue
                              image: ${registry}:latest
            EOF
            '''
        }
      }
    }
    stage('Switch Approval') {
      steps {
        input "Switch LIVE traffic to Blue Zone?"
      }
    }
    stage('Switch Live') {
      steps {
        withAWS(region:'us-west-2', credentials:'aws-static') {
            sh '''
            cat <<EOF | kubectl apply -f -
            apiVersion: v1
            kind: Service
            metadata:
                name: tmapp-lb
                labels:
                    app: tmapp-lb
            spec:
                type: LoadBalancer
                ports:
                - port: 5000
                  targetPort: 80
                  protocol: TCP
                  name: http
                selector:
                    app: blue
            EOF
            '''
        }
      }
    }
  }
}