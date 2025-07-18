Practica Bootcamp DevOps - Desafio 2
# Ejecucion mediante dockerfile
* Creacion de imagen del contenedor:

    <sub>docker build . -t gustavobarrera/flaskapp:v1</sub>
  
* Ejecución del contenedor previamente creado:
  
    <sub>docker run --name miapp-test -p 5000:5000 -v $(pwd)/user_data:/app/instance -d gustavobarrera/flaskapp
:v1</sub>

# Ejecucion mediante docker compose
* Una vez clonado el repositorio, dentro de la carpeta de trabajo ejecutamos:

    <sub>docker compose -f docker-compose.yaml up -d</sub>

# Pasos de instalacion del servidor de Jenkins para la ejecucion de un pipeline
* Instalacion del servidor y permisos para poder utilizar docker en el host

    <sub>docker run -p 8080:8080 -p 50000:50000 -d --name jenkinsv1 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home --restart=always jenkins/jenkins:alpine</sub>

* Conectarse al contenedor con usuario root

    <sub>docker exec -it --user root jenkinsv1 sh</sub>

* Instalar Docker en Jenkins

    <sub>apk update apk add docker-cli</sub>

* Validar grupo Docker

    <sub>ls -l /var/run/docker.sock</sub>

* Crear grupo Docker y agregar usuario Jenkins al grupo Docker

    <sub>addgroup docker</sub>

    <sub>addgroup jenkins docker</sub>

    <sub>chgrp docker /var/run/docker.sock</sub>

    <sub>chmod 660 /var/run/docker.sock</sub>

    <sub>docker restart jenkinsv1</sub>
    
# Documento de configuración del servidor Jenkins para la ejecución del pipeline.

https://docs.google.com/document/d/1iQVxnoG54x1BYiXkob31yWrPGQTlKr4O4yhW5Bw6iII/edit?usp=sharing
