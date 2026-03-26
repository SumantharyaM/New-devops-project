pipeline {
    agent { label 'agent-1' }

    environment {
        DOCKERHUB_CREDS = credentials('docker-creds')
        IMAGE_NAME = 'sumantharya/devops-app'
        TMPDIR = '/home/ec2-user/tmp'
        S3_BUCKET = 'devops-trivy-reports'
    }

    stages {

        stage('Clone Code') {
            steps {
                git 'https://github.com/SumantharyaM/New-devops-project.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo Build Started...'
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                docker build -t devops-app ./backend
                '''
            }
        }

        stage('Docker Tag') {
            steps {
                sh '''
                docker tag devops-app $IMAGE_NAME:latest
                '''
            }
        }

        stage('Docker Login & Push') {
            steps {
                sh '''
                echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin
                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Trivy Scan (JSON Report)') {
            steps {
                sh '''
                mkdir -p $TMPDIR
                trivy image \
                  --cache-dir $TMPDIR \
                  --format json \
                  -o trivy-report.json \
                  devops-app
                '''
            }
        }

        stage('Upload Report to S3') {
            steps {
                sh '''
                aws s3 cp trivy-report.json s3://$S3_BUCKET/
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'trivy-report.json', fingerprint: true
        }
        success {
            echo "Pipeline SUCCESS 🚀"
        }
        failure {
            echo "Pipeline FAILED ❌"
        }
    }
}
