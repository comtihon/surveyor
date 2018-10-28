#!/bin/bash

function build {
    if [[ ! "$(docker images -q com.surveyor.$1)" ]]
    then
        echo "building $1"
        mkdir -p services
        cd services && git clone https://github.com/comtihon/survey_$1
        cd survey_$1 && ./gradlew build buildDocker;\
        cd ../../
    else
        echo "skipping $1 build"
    fi;
}

build manager
build statistics
build requests
build collector

docker build -t surveyor .