pipeline {
    agent any

    environment {
        PYTHON_IMG_NAME = "python-app:${BUILD_NUMBER}"
        NGINX_IMG_NAME = "nginx-static:${BUILD_NUMBER}"
        DOCKER_REGISTRY = "etcsys"
        SSH_PRIVATE_KEY = credentials('c9e48fbe-2820-4f9b-8bf4-36ab119f3e31') // Replace with your SSH private key credentials ID
    }

    stages {
        stage('Setup Docker Buildx') {
            steps {
                sh '''
                    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
                    docker buildx create --name mybuilder
                    docker buildx use mybuilder
                '''
            }
        }
        
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
                // Run apt-get update with SSH agent
                sshagent(['c9e48fbe-2820-4f9b-8bf4-36ab119f3e31']) { // Use your SSH private key credentials ID here
                    sh 'sudo apt-get update'
                }
            }
        }

        stage('Snyk Security Scan') {
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    script {
                        // Ensure .snyk file is present in the workspace
                        sh 'ls -l /home/etcsys/project-int/.snyk' // Check if .snyk file exists
                        sh 'cp /home/etcsys/project-int/.snyk .'   // Copy .snyk file to current directory

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
