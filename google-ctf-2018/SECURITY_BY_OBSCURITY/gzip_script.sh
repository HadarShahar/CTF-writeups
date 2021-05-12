#!/bin/sh
while :
do
echo 'new'
mv new new.gz
gzip -d new
done
