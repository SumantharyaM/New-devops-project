pipeline {
    agent any

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

    }
}
