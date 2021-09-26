#!/bin/bash

docker run -itd -p 20000:20000 --env-file chall.env -v `pwd`/contracts:/home/ctf/contracts -v `pwd`/info.yaml:/home/ctf/info.yaml chainflag/eth-challenge-base
