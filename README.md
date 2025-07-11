Practica Bootcamp DevOps
# Ejecucion mediante dockerfile
* Creacion de imagen del contenedor
  docker build . -t gustavobarrera/flaskapp:v1
* Ejecución del contenedor previamente creado
docker run --name miapp-test -p 5000:5000 -v $(pwd)/user_data:/app/instance -d gustavobarrera/flaskapp
:v1

<img width="733" height="92" alt="image" src="https://github.com/user-attachments/assets/1f885f1b-5389-4bd9-b291-3ca232257fda" />
