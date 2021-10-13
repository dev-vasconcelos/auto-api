#! /bin/bash

IMAGENAME=ProjectName/api:latest

EXPOSEDPORT=5001
PORT=5001

CONTAINERNAME=project-name-api

chmod +x dockerfile-generator.sh

./dockerfile-generator.sh

docker build -t $IMAGENAME .
# HOST : CONTAINER
docker run -ti --name $CONTAINERNAME -p $EXPOSEDPORT:$PORT $IMAGENAME

#docker run -tD --name $CONTAINERNAME -p 5001:$PORT $IMAGENAME

