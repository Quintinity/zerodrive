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
    COLOR=$(tput setaf 2)
    COLOR_RESET=$(tput sgr0)
    MSG=
    
    if [ "$code" != "$expected_code" ]; then
        RESULT="FAIL"
        COLOR=$(tput setaf 1)
        FAILED_TEST_CASES=$(($FAILED_TEST_CASES + 1))
    fi
    TOTAL_TEST_CASES=$(($TOTAL_TEST_CASES + 1))

    echo "[${COLOR}${RESULT}${COLOR_RESET}] ${title}"
}

testcase "Test user creation" 200 curl -s -H "Content-Type: application/json" -X POST -d '{"vmarica": "a"}' $BASEURL/user

if [[ $FAILED_TEST_CASES -gt 0 ]]; then
    exit 1
fi