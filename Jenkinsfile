pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io/etcsys'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        IMAGE_NAME = 'project-int'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'etcsys_test', url: 'https://github.com/cerform/project-int.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Create and activate a virtual environment
                    sh 'python -m venv venv'
                    sh 'source venv/bin/activate'

                    // Install project dependencies
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Ensure virtual environment is activated
                    sh 'source venv/bin/activate'

                    // Run tests using pytest
                    sh 'pytest --junitxml=report.xml'
                    junit 'report.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Ensure virtual environment is activated
                    sh 'source venv/bin/activate'

                    // Build Docker image
                    def imageTag = "latest"
                    sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${imageTag} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Ensure virtual environment is activated
                    sh 'source venv/bin/activate'

                    // Push Docker image to registry
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                        def imageTag = "latest"
                        sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${imageTag}"
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace after pipeline execution
            cleanWs()
        }
    }
}
