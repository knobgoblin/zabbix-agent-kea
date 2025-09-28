#!/bin/sh

mydir=$(basename $0)
packaging_dir=$mydir/packaging/DEBIAN
prefix=/usr/local

mkdir -p ${packaging_dir}${prefix}/{bin,etc}
cp $mydir/zabbix-agent-kea.py ${packaging_dir}{$prefix}/bin
cp $mydir/zabbix-agent-kea.conf.yaml ${packaging_dir}{$prefix}/etc

dpkg-deb --build $mydir/packaging zabbix-agent-kea_0.1.deb
