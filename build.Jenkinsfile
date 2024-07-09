pipeline {
    agent any

    environment {
        DOCKER_CLI_EXPERIMENTAL = 'enabled' // Required for Docker Buildx
        PATH = "${tool 'docker'}:${env.PATH}" // Ensure Docker binaries are in PATH
        PYTHON_IMG_NAME = "python-app:${BUILD_NUMBER}"
        NGINX_IMG_NAME = "nginx-static:${BUILD_NUMBER}"
        DOCKER_REGISTRY = "etcsys"
        SSH_PRIVATE_KEY = credentials('c9e48fbe-2820-4f9b-8bf4-36ab119f3e31') // Replace with your SSH private key credentials ID
    }

    stages {
        stage('List Builders') {
            steps {
                script {
                    sh 'docker buildx ls'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        // Build and push Python app image
                        sh '''
                            echo $USERPASS | docker login -u $USERNAME --password-stdin
                            docker buildx build --platform linux/amd64,linux/arm64 -t $DOCKER_REGISTRY/$PYTHON_IMG_NAME -f /home/etcsys/project-int/Dockerfile.python /home/etcsys/project-int
                            docker buildx build --platform linux/amd64,linux/arm64 -t $DOCKER_REGISTRY/$NGINX_IMG_NAME -f /home/etcsys/project-int/Dockerfile.nginx /home/etcsys/project-int
                        '''
                        // Tag and push images
                        sh '''
                            docker buildx imagetools create $DOCKER_REGISTRY/$PYTHON_IMG_NAME --tag $DOCKER_REGISTRY/$PYTHON_IMG_NAME
                            docker buildx imagetools create $DOCKER_REGISTRY/$NGINX_IMG_NAME --tag $DOCKER_REGISTRY/$NGINX_IMG_NAME
                        '''
                        // Push images
                        sh '''
                            docker buildx imagetools push $DOCKER_REGISTRY/$PYTHON_IMG_NAME
                            docker buildx imagetools push $DOCKER_REGISTRY/$NGINX_IMG_NAME
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
                        sh 'ls -l /home/etcsys/project-int/snyk-ignore.txt' // Check if .snyk file exists
                        sh 'cp /home/etcsys/project-int/snyk-ignore.txt .'   // Copy .snyk file to current directory

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
