#!/bin/sh
while :
do
echo 'new'
bzip2 -d new
mv new.out new
done
