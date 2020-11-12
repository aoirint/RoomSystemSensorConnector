#!/bin/bash

./compose.sh down
./build.sh
./compose.sh up -d
./compose.sh logs -f

