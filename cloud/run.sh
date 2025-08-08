#!/bin/bash

# Detener y eliminar el contenedor si existe
if [ "$(docker ps -aq -f name=cloud_app)" ]; then
    docker stop cloud_app
    docker rm cloud_app
fi

# Eliminar la imagen si existe
if [ "$(docker images -q cloud)" ]; then
    docker rmi cloud
fi

# Construir la imagen
docker build -t cloud .

# Ejecutar el contenedor
docker run -d -p 8001:8001 --name cloud_app cloud
