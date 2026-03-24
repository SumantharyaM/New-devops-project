pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('docker-creds')
    }

    stages {

        stage('Clone Check') {
            steps {
                echo "Code cloned successfully"
            }
        }

        stage('Build Test') {
            steps {
                sh 'echo Build stage running'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t devops-app ./backend'
            }
        }

        stage('Trivy Scan') {
            steps {
                sh 'trivy image devops-app'
            }
        }

        stage('Docker Tag') {
            steps {
                sh 'docker tag devops-app sumantharya/devops-app:latest'
            }
        }

        stage('Docker Push') {
            steps {
                sh '''
                echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin
                docker push sumantharya/devops-app:latest
                '''
            }
        }

    }
}
