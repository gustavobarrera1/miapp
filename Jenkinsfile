pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'gustavobarrera/miapp-web'
        DOCKER_TAG = "v${sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()}" // Agrega secuencialidad x cada commit
        DOCKER_CREDENTIALS_ID = 'dockerhub_id' // 
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
                    def estado = sh(
                        script: "docker inspect -f '{{.State.Status}}' ${CONTAINER_NAME}",
                        returnStdout: true
                    ).trim()

                    def pausado = sh(script: "docker inspect -f '{{.State.Paused}}' ${CONTAINER_NAME}", returnStdout: true).trim()
                    def reiniciando = sh(script: "docker inspect -f '{{.State.Restarting}}' ${CONTAINER_NAME}", returnStdout: true).trim()
                    def muerto = sh(script: "docker inspect -f '{{.State.Dead}}' ${CONTAINER_NAME}", returnStdout: true).trim()

                    if (pausado == "true" || reiniciando == "true" || muerto == "true") {
                        error("El contenedor '${CONTAINER_NAME}' está fallando (Paused, Restarting o Dead).")
                    } else if (estado != "running") {
                        error("El contenedor '${CONTAINER_NAME}' no está en estado 'running'. Estado actual: '${estado}'.")
                    } else {
                        echo "El contenedor está en buen estado y en ejecución (running)."
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