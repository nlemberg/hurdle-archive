pipeline {
    agent any
    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }
    
    environment {
        TEST_NET = 'jenkins-test-net'
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
                sh 'docker build -t hurdle-archive .'
            }
        }
        // stage('Run Container'){
        //     steps {
        //         sh """
        //             echo 'running container'
        //             if [ \$(docker ps -q -f name=hurdle-archive) ]; then
        //                 echo 'Stopping and removing existing hurdle-archive container'
        //                 docker stop hurdle-archive
        //                 docker rm hurdle-archive
        //             fi
        //             docker run --name hurdle-archive --network "jenkins_network" -p 5000:5000 -d hurdle-archive
        //         """
        //     }
        // }
        stage('Run'){
            steps {
                export TEST_NET=${TEST_NET}
                sh 'docker-compose up -d'
            }
        }
        stage('Test Container'){
            steps {
                retry(15) {
                sleep(time: 3, unit: 'SECONDS')
                sh """
                    docker run --rm --network ${TEST_NET} \
                        docker.io/curlimages/curl:latest \
                        -fsSLI http://nginx:80/health
                """
                }
            }
        }
        stage('Destroy'){
            steps {
                sh 'docker-compose down -v'
            }
        }
        // stage('Destroy'){
        //     steps {
        //         sh 'echo "removing hurdle-archive container and image"'
        //         sh 'docker stop hurdle-archive'
        //         sh 'docker rm hurdle-archive'
        //         sh 'docker rmi hurdle-archive'
        //     }
        // }
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