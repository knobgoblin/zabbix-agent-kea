#!/bin/bash

mydir=$(dirname $0)

$mydir/mock-server.sh &
mock_pid=$!
trap 'kill -9 $mock_pid 2>/dev/null' INT TERM EXIT
echo "Mock server running as PID $mock_pid."
echo

pytest
