#!/bin/bash

docker swarm init --advertise-addr 127.0.0.1

docker-compose -f stack.yml build
docker stack deploy -c stack.yml scd3