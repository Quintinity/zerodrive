#!/bin/bash
HOST=http://127.0.0.1:40500

set -x

function testcase() {
    shift;
    shift;
    result=$("$@")
    echo result
}

testcase "Test user creation" 200 curl -s -H "Content-Type: application/json" -X POST -d '{"vmarica": "a"}' $HOST/user