pipeline {
    agent { label 'agent-1' }

    environment {
        DOCKERHUB_CREDS = credentials('docker-creds')
        IMAGE_NAME = 'sumantharya/devops-app'
        TMPDIR = '/home/ec2-user/tmp'
        S3_BUCKET = 'devops-trivy-reports'
    }

    stages {

        stage('Build') {
            steps {
                sh 'echo Build Started...'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t devops-app ./backend'
            }
        }

        stage('Docker Tag') {
            steps {
                sh 'docker tag devops-app $IMAGE_NAME:latest'
            }
        }

        stage('Docker Push') {
            steps {
                sh '''
                echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin
                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Trivy Scan') {
            steps {
                sh '''
                mkdir -p $TMPDIR
                trivy image --cache-dir $TMPDIR --format json -o trivy-report.json devops-app
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                sh 'aws s3 cp trivy-report.json s3://$S3_BUCKET/'
            }
        }
    }
}
