pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gustavobarrera/miapp-web'
        DOCKER_TAG = "v${sh(script: 'git rev-list --count HEAD', returnStdout: true).trim()}" // Agrega secuencialidad x cada commit
        DOCKER_CREDENTIALS_ID = 'dockerhub_id' // Jenkins credentials ID
        COMPOSE_FILE = 'docker-compose.yaml'
        CONTAINER_NAME = 'miapp-test'
    }

    stages {
        stage('Clonar código') {
            steps {
                checkout scm
            }
        }

        stage('Construir imagen Docker') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Iniciar contenedor con Docker Compose') {
            steps {
                script {
                    sh """
                    docker compose -f ${COMPOSE_FILE} up -d --force-recreate
                    """
                }
            }
        }

        stage('Verificar estado del contenedor') {
            steps {
                script {
                    def estadoContenedor = sh(
                        script: """"
                            if docker inspect -f '{{.State.Paused}}' ${COMPOSE_FILE} | grep true || \
                               docker inspect -f '{{.State.Restarting}}' ${COMPOSE_FILE} | grep true || \
                               docker inspect -f '{{.State.Dead}}' ${COMPOSE_FILE} | grep true; then
                               exit 1
                            fi
                        """"",
                        returnStatus: true
                    )

                    if (estadoContenedor != 0) {
                        error("El contenedor '${COMPOSE_FILE}' está en un estado roto (Paused, Restarting o Dead).")
                    } else {
                        echo "El contenedor está en buen estado."
                    }
                }
            }
        }
        

        stage('Login en Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        echo 'Login exitoso en Docker Hub'
                    }
                }
            }
        }

        stage('Push a Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        def image = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                        image.push()
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Imagen publicada en Docker Hub: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
        failure {
            echo "Error en el pipeline"
        }
    }
}