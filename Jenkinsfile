pipeline {
    agent any

    environment {
        IMG_NAME = "jenkinsfile-${BUILD_NUMBER}"
    }

    stages {
        stage('Build docker image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        bat '''
                            echo $USERPASS | docker login -u %USERNAME% --password-stdin
                            docker build -t %IMG_NAME% .
                            docker tag %IMG_NAME% etcsys/%IMG_NAME%
                            docker push etcsys/%IMG_NAME%
                        '''
                    }
                }
            }
        }
    }
}
