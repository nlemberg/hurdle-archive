pipeline {
    agent any
    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }
    
    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t hurdle-img .'
            }
        }
        stage('Run Container'){
            steps {
                sh """
                    echo 'running container'
                    if [ \$(docker ps -q -f name=hurdle-archive) ]; then
                        echo 'Stopping and removing existing hurdle-archive container'
                        docker stop hurdle-archive
                        docker rm hurdle-archive
                    fi
                    docker run --name hurdle-archive --network "jenkins_network" -p 5000:5000 -d hurdle-img
                """
            }
        }
        stage('Test Container') {
            steps {
                script {
                    def attempts = 7

                    while (attempts > 0) {
                        def httpStatus = sh(script: 'curl -Is http://hurdle-archive:5000 | head -n 1 | awk \'{print $2}\'', returnStatus: true).trim()

                        if (httpStatus == "302") {
                            echo "hurdle-archive app is up and running"
                            break
                        } else {
                            sleep 3
                            attempts--
                        }
                    }

                    if (attempts == 0) {
                        echo "Could not connect to hurdle-archive app (status ${httpStatus})"
                    }
                }
            }
        }
        stage('Destroy'){
            steps {
                sh "removing hurdle-archive container and image"
                sh 'docker stop hurdle-archive'
                sh 'docker rm hurdle-archive'
                sh 'docker rmi hurdle-img'
            }
        }
    }
    post {
        always {
            cleanWs(deleteDirs: true)
            sh '''
                docker image prune -af
                docker volume prune -af
                docker container prune -f
                docker network prune -f
            '''
        }
    }
}