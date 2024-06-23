pipeline {
    agent any

    environment {
        PYTHON_IMG_NAME = "python-app:${BUILD_NUMBER}"
        NGINX_IMG_NAME = "nginx-static:${BUILD_NUMBER}"
    }

    stages {
        stage('Build Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        // Build and push Python app image
                        sh '''
                            echo $USERPASS | docker login -u $USERNAME --password-stdin
                            docker build -t $PYTHON_IMG_NAME -f Dockerfile.python .
                            docker tag $PYTHON_IMG_NAME exaclly/$PYTHON_IMG_NAME
                            docker push exaclly/$PYTHON_IMG_NAME
                        '''
                        // Build and push Nginx image
                        sh '''
                            echo $USERPASS | docker login -u $USERNAME --password-stdin
                            docker build -t $NGINX_IMG_NAME -f Dockerfile.nginx .
                            docker tag $NGINX_IMG_NAME exaclly/$NGINX_IMG_NAME
                            docker push exaclly/$NGINX_IMG_NAME
                        '''
                    }
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                script {
                    def dockerComposeContent = """
                    version: '3.8'

                    services:
                      python_app:
                        image: exaclly/$PYTHON_IMG_NAME
                        ports:
                          - "8000:8000"

                      nginx:
                        image: exaclly/$NGINX_IMG_NAME
                        ports:
                          - "80:80"
                    """
                    writeFile file: 'docker-compose.yaml', text: dockerComposeContent
                    sh 'docker-compose down'
                    sh 'docker-compose up -d'
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