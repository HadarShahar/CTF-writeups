#!/bin/sh
for i in $(seq 1 50) 
do
echo $i
mv password* $i.zip
unzip $i.zip
done
