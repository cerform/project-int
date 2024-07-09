pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io/etcsys'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        IMAGE_NAME = 'project-int'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout SCM steps
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                // Install Python virtual environment
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                // Example of running Python tests
                sh '''
                source venv/bin/activate
                python -m unittest discover -s tests
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Build Docker image steps
                script {
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:latest")
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                // Push Docker image steps
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_CREDENTIALS_ID}") {
                        docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:latest").push()
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
