#!/bin/sh

mydir=$(dirname $0)
rm -rf $mydir/packaging/DEBIAN/usr
rm -rf $mydir/zabbix-agent-kea_*.deb