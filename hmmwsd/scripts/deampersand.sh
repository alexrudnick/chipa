#!/bin/bash

cp $1 beforedeampersand
sed 's/\&/AMPERSAND/g' $1 > /tmp/deampersand
mv /tmp/deampersand $1
