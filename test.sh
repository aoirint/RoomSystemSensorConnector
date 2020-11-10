#!/bin/bash

docker-compose down
./build.sh

docker-compose run --rm app python3 /code/test_MyEventHandler.py

docker-compose down

