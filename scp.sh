#!/bin/bash -eu

cd $(dirname $0)
HERE=`pwd`
DST='pi@iotbox.local:~/iot'
scp $HERE/* $DST