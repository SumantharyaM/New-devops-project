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

        stage('Docker Login & Push') {
            steps {
                sh '''
                echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin
                docker push $IMAGE_NAME:latest
                '''
            }
        }

        stage('Trivy Scan (JSON + HTML)') {
            steps {
                sh '''
                mkdir -p $TMPDIR

                # JSON report
                trivy image \
                  --cache-dir $TMPDIR \
                  --format json \
                  -o trivy-report.json \
                  devops-app

                # HTML report
                trivy image \
                  --cache-dir $TMPDIR \
                  --format template \
                  --template "@/usr/local/share/trivy/templates/html.tpl" \
                  -o trivy-report.html \
                  devops-app
                '''
            }
        }

        stage('Fail on CRITICAL Vulnerabilities') {
            steps {
                sh '''
                CRITICAL_COUNT=$(cat trivy-report.json | grep -o '"Severity":"CRITICAL"' | wc -l)

                echo "Critical Vulnerabilities: $CRITICAL_COUNT"

                if [ "$CRITICAL_COUNT" -gt 0 ]; then
                    echo "❌ CRITICAL vulnerabilities found! Failing build..."
                    exit 1
                else
                    echo "✅ No CRITICAL vulnerabilities"
                fi
                '''
            }
        }

        stage('Upload Reports to S3') {
            steps {
                sh '''
                aws s3 cp trivy-report.json s3://$S3_BUCKET/
                aws s3 cp trivy-report.html s3://$S3_BUCKET/
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'trivy-report.*', fingerprint: true
        }
        success {
            echo "Pipeline SUCCESS 🚀"
        }
        failure {
            echo "Pipeline FAILED due to vulnerabilities ❌"
        }
    }
}
