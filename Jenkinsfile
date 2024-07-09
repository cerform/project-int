pipeline {
    agent any // Use 'any' agent type if not specifying a specific Jenkins node or Docker image

    stages {
        stage('Build') {
            agent {
                docker {
                    image 'your-docker-agent-image'
                    args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''
                    docker build -t project-int-app:latest ./app
                    docker build -t project-int-web:latest ./web
                '''
            }
        }
        stage('Test') {
            agent any // You can use 'any' here if tests do not require specific Docker environment
            steps {
                sh 'python -m pytest'
            }
        }
        stage('Security Scan') {
            agent any // Again, 'any' agent type for flexibility
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    sh 'snyk container test project-int-app:latest'
                    sh 'snyk container test project-int-web:latest'
                }
            }
        }
        stage('Deploy') {
            agent any // 'any' agent type if deployment does not need a specific Docker environment
            steps {
                sh '''
                    docker login -u <your-docker-username> -p <your-docker-password>
                    docker push project-int-app:latest
                    docker push project-int-web:latest
                '''
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
