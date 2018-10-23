#!/bin/bash
IP=127.0.0.1
PORT=40500
BASEURL=http://$IP:$PORT

COOKIE_JAR="-b cookiejar -c cookiejar"

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
    COLOR=$(tput setaf 2 2>/dev/null)
    COLOR_RESET=$(tput sgr0 2>/dev/null)
    MSG=
    
    if [ "$code" != "$expected_code" ]; then
        RESULT="FAIL"
        COLOR=$(tput setaf 1 2>/dev/null)
        FAILED_TEST_CASES=$(($FAILED_TEST_CASES + 1))
    fi
    TOTAL_TEST_CASES=$(($TOTAL_TEST_CASES + 1))

    echo "[${COLOR}${RESULT}${COLOR_RESET}] ${title}"
}

# Account creation tests
testcase "Test user creation - no email"    400 curl -s -H "Content-Type: application/json" -X POST -d '{"password": "a@unb.ca"}' $BASEURL/user
testcase "Test user creation - no password" 400 curl -s -H "Content-Type: application/json" -X POST -d '{"email": "abcdef"}' $BASEURL/user
testcase "Test user creation - normal"  200 curl -s -H "Content-Type: application/json" -X POST -d '{"email": "user@unb.ca", "password": "abcdef"}' $BASEURL/user
testcase "Test user creation - duplicate"   400 curl -s -H "Content-Type: application/json" -X POST -d '{"email": "user@unb.ca", "password": "xyzabc"}' $BASEURL/user

# Login/logout tests
testcase "Test logging in" 200 curl -s $COOKIE_JAR -H "Content-Type: application/json" -X POST -d '{"email": "user@unb.ca", "password": "abcdef"}' $BASEURL/login
testcase "Test logging out" 200 curl -s $COOKIE_JAR -X DELETE $BASEURL/login

# Login and delete the account
curl -s $COOKIE_JAR -H "Content-Type: application/json" -X POST -d '{"email": "user@unb.ca", "password": "abcdef"}' $BASEURL/login
testcase "Account deletion - normal"        200 curl -s $COOKIE_JAR -X DELETE $BASEURL/user
testcase "Account deletion - not logged in" 401 curl -s $COOKIE_JAR -X DELETE $BASEURL/user


if [[ $FAILED_TEST_CASES -gt 0 ]]; then
    exit 1
fi

