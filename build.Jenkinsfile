pipeline {
    agent any

    environment {
        PYTHON_IMG_NAME = "python-app:${BUILD_NUMBER}"
        NGINX_IMG_NAME = "nginx-static:${BUILD_NUMBER}"
        DOCKER_REGISTRY = "exaclly"
    }

    stages {
        stage('Build Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'etcsys', passwordVariable: '055658273')]) {
                    script {
                        // Build and push Python app image
                        sh '''
                            export DOCKER_REGISTRY=${DOCKER_REGISTRY}
                            export USERPASS=${USERPASS}
                            export USERNAME=${USERNAME}
                            export PYTHON_IMG_NAME=${PYTHON_IMG_NAME}
                            echo $USERPASS | docker login -u $USERNAME --password-stdin
                            docker build -t $PYTHON_IMG_NAME -f Dockerfile.python .
                            docker tag $PYTHON_IMG_NAME $DOCKER_REGISTRY/$PYTHON_IMG_NAME
                            docker push $DOCKER_REGISTRY/$PYTHON_IMG_NAME
                        '''
                        // Build and push Nginx image
                        sh '''
                            export DOCKER_REGISTRY=${DOCKER_REGISTRY}
                            export USERPASS=${USERPASS}
                            export USERNAME=${USERNAME}
                            export NGINX_IMG_NAME=${NGINX_IMG_NAME}
                            echo $USERPASS | docker login -u $USERNAME --password-stdin
                            docker build -t $NGINX_IMG_NAME -f Dockerfile.nginx .
                            docker tag $NGINX_IMG_NAME $DOCKER_REGISTRY/$NGINX_IMG_NAME
                            docker push $DOCKER_REGISTRY/$NGINX_IMG_NAME
                        '''
                    }
                }
            }
        }

        stage('Snyk Security Scan') {
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    script {
                        // Scan Python app image
                        sh '''
                            export SNYK_TOKEN=${SNYK_TOKEN}
                            export DOCKER_REGISTRY=${DOCKER_REGISTRY}
                            export PYTHON_IMG_NAME=${PYTHON_IMG_NAME}
                            snyk auth $SNYK_TOKEN
                            snyk container test $DOCKER_REGISTRY/$PYTHON_IMG_NAME
                        '''
                        // Scan Nginx image
                        sh '''
                            export SNYK_TOKEN=${SNYK_TOKEN}
                            export DOCKER_REGISTRY=${DOCKER_REGISTRY}
                            export NGINX_IMG_NAME=${NGINX_IMG_NAME}
                            snyk auth $SNYK_TOKEN
                            snyk container test $DOCKER_REGISTRY/$NGINX_IMG_NAME
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
                        image: $DOCKER_REGISTRY/$PYTHON_IMG_NAME
                        ports:
                          - "8000:8000"

                      nginx:
                        image: $DOCKER_REGISTRY/$NGINX_IMG_NAME
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
