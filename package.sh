#!/bin/sh

mydir=$(dirname $0)
packaging_dir=$mydir/packaging/DEBIAN
prefix=/usr/local

echo "Creating package:"
echo "  -> Using workspace $packaging_dir ..."
mkdir -p ${packaging_dir}$prefix/{bin,etc}
echo "  -> Copying agent to ${packaging_dir}$prefix/bin ..."
cp $mydir/zabbix-agent-kea.py ${packaging_dir}$prefix/bin
echo "  -> Copying base configuration to ${packaging_dir}$prefix/etc ..."
cp $mydir/zabbix-agent-kea.conf.yaml ${packaging_dir}$prefix/etc

dpkg-deb --build $mydir/packaging zabbix-agent-kea_0.1.deb
