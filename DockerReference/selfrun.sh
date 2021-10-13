#! /bin/bash

IMAGENAME=owner/projeto:1

PORT=80

CONTAINERNAME=containerApplicatio2n

chmod +x dockerfile-generator.sh

./dockerfile-generator.sh

docker build -t $IMAGENAME .
# HOST : CONTAINER
docker run -ti --name $CONTAINERNAME -p 5001:$PORT $IMAGENAME

#docker run -tD --name $CONTAINERNAME -p 5001:$PORT $IMAGENAME

