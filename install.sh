#!/bin/bash -eu

cd $(dirname $0)
SERVICE=iotbox.service
DST=/etc/systemd/system/$SERVICE

if [ -f $DST ]; then
  systemctl disable $SERVICE
  rm $DST
fi

cp $SERVICE $DST
systemctl enable $SERVICE
systemctl start $SERVICE
