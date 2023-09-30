#!/bin/bash

case $1 in
    -h)
        printf "This script will install the necessary python dependencies needed for this controller interface\n"
    ;;
    *)
        pip3 install pyserial 
    ;;

esac