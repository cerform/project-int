pipeline {
    agent any // Use 'any' agent type if not specifying a specific Jenkins node or Docker image

    stages {
        stage('Build') {
            agent {
                docker {
                    image 'your-docker-agent-image' // Replace with your desired base Docker image
                    args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh '''
                    docker build -t etcsys/project-int-app:latest ./app
                    docker build -t etcsys/project-int-web:latest ./web
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
                    sh 'snyk container test etcsys/project-int-app:latest'
                    sh 'snyk container test etcsys/project-int-web:latest'
                }
            }
        }
        stage('Deploy') {
            agent any // 'any' agent type if deployment does not need a specific Docker environment
            environment {
                DOCKER_CRED = credentials('docker-hub-credentials')
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CRED) {
                        docker.image('etcsys/project-int-app:latest').push()
                        docker.image('etcsys/project-int-web:latest').push()
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
