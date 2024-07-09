pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io/etcsys'
        DOCKER_CREDENTIALS_ID = 'docker-hub-credentials'
        IMAGE_NAME = 'project-int'
        PYTHON_HOME = tool name: 'Python3', type: 'hudson.plugins.python.PythonInstallation'
        PATH = "${PYTHON_HOME}/bin:${env.PATH}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'etcsys_test', url: 'https://github.com/cerform/project-int.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'source venv/bin/activate && pytest --junitxml=report.xml'
                junit 'report.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "latest"
                    sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${imageTag} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
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
            cleanWs()
        }
    }
}
