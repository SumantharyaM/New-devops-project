pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('docker-creds')
        BUCKET_NAME = 'devops-trivy-reports'
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
                sh '''
                mkdir -p /var/lib/jenkins/trivy-temp
                export TMPDIR=/var/lib/jenkins/trivy-temp

                trivy image --scanners vuln -f json -o trivy-report.json devops-app
                '''
            }
        }

        stage('Upload Report to S3') {
            steps {
                sh '''
                aws s3 cp trivy-report.json s3://$BUCKET_NAME/trivy-report-$(date +%s).json
                '''
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

    post {
        always {
            archiveArtifacts artifacts: 'trivy-report.json', fingerprint: true
        }
    }
}
