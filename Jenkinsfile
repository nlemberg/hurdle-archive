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
        stage('Test Container'){
            steps {
                sh """
                    attempts=7
                    http_status=

                    while [ \$attempts -gt 0 ]; do
                    http_status=\$(curl -Is http://hurdle-archive:5000 | head -n 1)
                    if [ \$http_status ==~ \/\^HTTP/1.1 302 FOUND\/ ]; then
                        echo "hurdle-archive app is up and running"
                        break
                    else
                        sleep 3
                        attempts=\$((attempts - 1))
                    fi
                    done

                    if [ \$attempts -eq 0 ]; then
                    echo "Could not connect to hurdle-archive app (status \$http_status)"
                    fi
                """
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