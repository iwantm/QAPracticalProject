#! /bin/bash

docker-compose down --rmi all
docker-compose build
docker login
docker-compose push