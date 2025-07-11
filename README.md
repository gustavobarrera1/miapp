Practica Bootcamp DevOps
# Ejecucion mediante dockerfile
* Creacion de imagen del contenedor:

docker build . -t gustavobarrera/flaskapp:v1
  
* Ejecución del contenedor previamente creado:
  
docker run --name miapp-test -p 5000:5000 -v $(pwd)/user_data:/app/instance -d gustavobarrera/flaskapp
:v1

# Ejecucion mediante docker compose
* Una vez clonado el repositorio, dentro de la carpeta de trabajo ejecutamos:

docker compose -f docker-compose.yaml up -d

# Pasos de instalacion del servidor de Jenkins para la ejecucion de un pipeline
* Instalacion del servidor y permisos para poder utilizar docker en el host

docker run -p 8080:8080 -p 50000:50000 -d --name jenkinsv1 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home --restart=always jenkins/jenkins:alpine

* Conectarse al contenedor con usuario root

docker exec -it --user root jenkinsv1 sh

* Instalar Docker en Jenkins

apk update apk add docker-cli

* Validar grupo Docker

ls -l /var/run/docker.sock

* Crear grupo Docker y agregar usuario Jenkins al grupo Docker

addgroup docker

addgroup jenkins docker

chgrp docker /var/run/docker.sock

chmod 660 /var/run/docker.sock

docker restart jenkinsv1

  
  
