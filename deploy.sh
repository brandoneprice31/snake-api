#!/bin/bash

if [ $1 != "production" ] ;
then
  echo env must be production
  exit
fi

# aws ecr get-login
docker build -t snake:$1 .;
docker tag snake:$1 832531170141.dkr.ecr.us-east-2.amazonaws.com/snake:$1;
docker push 832531170141.dkr.ecr.us-east-2.amazonaws.com/snake:$1;

~/src/ecs-deploy/./ecs-deploy -c bep-projects -n snake-$1-api -i 832531170141.dkr.ecr.us-east-2.amazonaws.com/snake:$1;
