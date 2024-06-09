pipeline {
    agent any

    environment {
        IMG_NAME = "Jenkinsfile:${BUILD_NUMBER}"
    }

    stages {
        stage('Build docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    sh '''
                        echo $USERPASS | docker login -u $USERNAME --password-stdin
                        docker build -t $IMG_NAME .
                        docker tag $IMG_NAME etcsys/$IMG_NAME
                        docker push etcsys/$IMG_NAME
                    '''
                }
            }
        }
    }
}

echo "test1"