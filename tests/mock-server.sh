#!/bin/bash

port=8000
body='[{"cache_item_value": "Response from Kea"}]'
length=$(printf '%s' "$body" | wc -c)

while true
do
  {
    printf 'HTTP/1.1 200 OK\r\n'
    printf 'Content-Type: application/json\r\n'
    printf 'Content-Length: %s\r\n' "$length"
    printf '\r\n'
    printf '%s' "$body"
  } | nc -l $port > /dev/null 2>&1
done