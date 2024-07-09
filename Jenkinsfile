pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io/etcsys'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        IMAGE_NAME = 'project-int'
    }

    tools {
        // Define Python installation
        python 'Python3'
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
                // Use Python tool to run commands
                sh "python -m venv venv"
            }
        }
        
        stage('Run Tests') {
            steps {
                // Example of running Python tests
                sh "python -m unittest discover -s tests"
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
                        dockerImage.push("${DOCKER_REGISTRY}/${IMAGE_NAME}:latest")
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                node {
                    // Clean up workspace
                    cleanWs()
                }
            }
        }
    }
}
