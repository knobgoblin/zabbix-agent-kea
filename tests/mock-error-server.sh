#!/bin/bash

port=18002
body='[{"message": "Error from Kea"}]'
length=$(printf '%s' "$body" | wc -c)

while true
do
  {
    printf 'HTTP/1.1 400 Bad Request\r\n'
    printf 'Content-Type: application/json\r\n'
    printf 'Content-Length: %s\r\n' "$length"
    printf '\r\n'
    printf '%s' "$body"
  } | nc -l $port > /dev/null 2>&1
done
