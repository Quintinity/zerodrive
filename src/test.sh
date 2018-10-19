#!/bin/bash
IP=127.0.0.1
PORT=40500
BASEURL=http://$IP:$PORT

# Use netcat to scan port to check if the server is running
nc -z $IP $PORT
if [ "$?" = "1" ]; then
    echo "Server not running at $BASEURL"
    exit 1
fi

TOTAL_TEST_CASES=0
FAILED_TEST_CASES=0

function testcase() {
    title="$1"
    shift;
    expected_code="$1"
    shift;
    code=$("$@" -w "%{http_code}" -o /dev/null)

    RESULT=" OK "
    COLOR=$(tput -Txterm setaf 2)
    COLOR_RESET=$(tput -Txterm sgr0)
    MSG=
    
    if [ "$code" != "$expected_code" ]; then
        RESULT="FAIL"
        COLOR=$(tput setaf 1)
        FAILED_TEST_CASES=$(($FAILED_TEST_CASES + 1))
    fi
    TOTAL_TEST_CASES=$(($TOTAL_TEST_CASES + 1))

    echo "[${COLOR}${RESULT}${COLOR_RESET}] ${title}"
}

testcase "Test user creation - no email"    400 curl -s -H "Content-Type: application/json" -X POST -d '{"password": "a@unb.ca"}' $BASEURL/user
testcase "Test user creation - no password" 400 curl -s -H "Content-Type: application/json" -X POST -d '{"email": "abcdef"}' $BASEURL/user
testcase "Test user creation - valid data"  200 curl -s -H "Content-Type: application/json" -X POST -d '{"email": "god@unb.ca", "password": "abcdef"}' $BASEURL/user
testcase "Test user creation - duplicate"   400 curl -s -H "Content-Type: application/json" -X POST -d '{"email": "god@unb.ca", "password": "xyzabc"}' $BASEURL/user

if [[ $FAILED_TEST_CASES -gt 0 ]]; then
    exit 1
fi

