pipeline {
    agent any

    environment {
        PYTHON_IMG_NAME = "python-app:${BUILD_NUMBER}"
        NGINX_IMG_NAME = "nginx-static:${BUILD_NUMBER}"
        SNYK_TOKEN = credentials('snyk-token') // Ensure you have a Jenkins credential with ID 'snyk-token'
    }

    stages {
        stage('Build Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        // Build and push Python app image
                        sh '''
                            echo "$USERPASS" | docker login -u "$USERNAME" --password-stdin
                            docker build -t "$PYTHON_IMG_NAME" -f Dockerfile.python .
                            docker tag "$PYTHON_IMG_NAME" etcsys/"$PYTHON_IMG_NAME"
                            docker push etcsys/"$PYTHON_IMG_NAME"
                        '''
                        // Build and push Nginx image
                        sh '''
                            echo "$USERPASS" | docker login -u "$USERNAME" --password-stdin
                            docker build -t "$NGINX_IMG_NAME" -f Dockerfile.nginx .
                            docker tag "$NGINX_IMG_NAME" etcsys/"$NGINX_IMG_NAME"
                            docker push etcsys/"$NGINX_IMG_NAME"
                        '''
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install pytest unittest2 pylint'
            }
        }

        stage('Parallel Linting and Unittest') {
            parallel {
                stage('Static Code Linting') {
                    steps {
                        sh 'python3 -m pylint -f parseable --reports=no *.py > pylint.log'
                    }
                    post {
                        always {
                            sh 'cat pylint.log'
                            recordIssues (
                                enabledForFailure: true,
                                aggregatingResults: true,
                                tools: [pyLint(name: 'Pylint', pattern: '**/pylint.log')]
                            )
                        }
                    }
                }
                stage('Unittest') {
                    steps {
                        script {
                            // Run unit tests
                            sh 'python3 -m pytest --junitxml results.xml tests/test_demo.py'
                        }
                    }
                    post {
                        always {
                            junit allowEmptyResults: true, testResults: 'results.xml'
                        }
                    }
                }
            }
        }

        stage('Snyk Scan Python Image') {
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    withEnv(["SNYK_TOKEN=${SNYK_TOKEN}"]) {
                        sh '''
                            snyk auth $SNYK_TOKEN
                            snyk container test etcsys/$PYTHON_IMG_NAME --file=Dockerfile.python --policy-path=.snyk
                        '''
                    }
                }
            }
        }

        stage('Snyk Scan Nginx Image') {
            steps {
                withCredentials([string(credentialsId: 'snyk-token', variable: 'SNYK_TOKEN')]) {
                    withEnv(["SNYK_TOKEN=${SNYK_TOKEN}"]) {
                        sh '''
                            snyk auth $SNYK_TOKEN
                            snyk container test etcsys/$NGINX_IMG_NAME --file=Dockerfile.nginx --policy-path=.snyk
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
                        image: etcsys/$PYTHON_IMG_NAME
                        ports:
                          - "8000:8000"

                      nginx:
                        image: etcsys/$NGINX_IMG_NAME
                        ports:
                          - "8445:8444"
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
            script {
                // Log the start of the cleanup process
                echo 'Starting cleanup process...'

                // Remove the built Docker images from the disk
                try {
                    sh '''
                        echo "Removing Docker image: etcsys/$PYTHON_IMG_NAME"
                        docker rmi etcsys/$PYTHON_IMG_NAME || echo "Image etcsys/$PYTHON_IMG_NAME already removed or not found."
                    '''
                } catch (Exception e) {
                    echo "Error during Docker image removal: ${e.getMessage()}"
                }

                try {
                    sh '''
                        echo "Removing Docker image: etcsys/$NGINX_IMG_NAME"
                        docker rmi etcsys/$NGINX_IMG_NAME || echo "Image etcsys/$NGINX_IMG_NAME already removed or not found."
                    '''
                } catch (Exception e) {
                    echo "Error during Docker image removal: ${e.getMessage()}"
                }

                // Clean the workspace
                cleanWs()

                // Log the end of the cleanup process
                echo 'Cleanup process completed.'
            }
        }
    }
}
