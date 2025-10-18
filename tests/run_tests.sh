#!/bin/bash

mydir=$(dirname $0)

$mydir/mock-server.sh &
mock_pid=$!
$mydir/mock-error-server.sh &
mock_error_pid=$!

trap 'kill -9 $mock_pid 2>/dev/null && kill -9 $mock_error_pid 2>/dev/null' INT TERM EXIT
echo
echo "Mock server running as PID $mock_pid."
echo "Mock error server running as PID $mock_error_pid."
echo

coverage run -m pytest -vv .
coverage xml -o ../coverage.xml
coverage html -d ../htmlcov
