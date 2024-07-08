pipeline {
    agent any

    environment {
        PYTHON_IMG_NAME = "python-app:${BUILD_NUMBER}"
        NGINX_IMG_NAME = "nginx-static:${BUILD_NUMBER}"
        DOCKER_REGISTRY = "etcsys"
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
                            docker tag $PYTHON_IMG_NAME $DOCKER_REGISTRY/$PYTHON_IMG_NAME
                            docker push $DOCKER_REGISTRY/$PYTHON_IMG_NAME
                        '''
                        // Build and push Nginx image
                        sh '''
                            echo $USERPASS | docker login -u $USERNAME --password-stdin
                            docker build -t $NGINX_IMG_NAME -f Dockerfile.nginx .
                            docker tag $NGINX_IMG_NAME $DOCKER_REGISTRY/$NGINX_IMG_NAME
                            docker push $DOCKER_REGISTRY/$NGINX_IMG_NAME
                        '''
                    }
                }
            }
        }

        stage('Update Dependencies') {
            steps {
                script {
                    // Run apt-get update with sudo
                    sh '''
                        sudo apt-get update
                    '''
                }
            }
        }

        stage('Snyk Security Scan') {
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    script {
                        // Ensure .snyk file is present in the workspace
<<<<<<< HEAD
                        sh 'ls -l /home/etcsys/project-int/.snyk' // Check if .snyk file exists
                        sh 'cp /home/etcsys/project-int/.snyk .'   // Copy .snyk file to current directory
=======
                        sh 'cp /home/etcsys/project-int/.snyk .'
>>>>>>> origin/main

                        // Authenticate with Snyk and run container security tests
                        sh '''
                            snyk auth $SNYK_TOKEN
                            snyk container test $DOCKER_REGISTRY/$PYTHON_IMG_NAME --file=.snyk
                            snyk container test $DOCKER_REGISTRY/$NGINX_IMG_NAME --file=.snyk
                        '''
                    }
                }
            }
        }
    }
}
