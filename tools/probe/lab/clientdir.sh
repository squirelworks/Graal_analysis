#!/bin/sh
# clientdir.sh BUILD : the folder under ~/fz12/cl holding that build
case $1 in 121) echo graal121i;; 139|138|137|136|135|134|133|132|131) echo graal$1;; 13) echo graal13b;; 128) echo graal128b2;;
  119) echo graal1.1.9;; 11) echo graal1.1;; 1st) echo 1stgraal;; 4thalpha|5thalpha|9thalpha) echo ${1%alpha}graalalpha;; *) echo ${1}graal;; esac
