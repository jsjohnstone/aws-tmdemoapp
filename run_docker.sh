#!/usr/bin/env bash

docker build --tag=jsjohnstone/tm-app .
docker run -p 5000:5000/tcp --env-file ./env.list jsjohnstone/tm-app:latest