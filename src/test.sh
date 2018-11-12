#!/bin/bash
IP=127.0.0.1
PORT=40500
BASEURL=https://$IP:$PORT

COOKIE_JAR_FILE="cookiejar.bin"
CURL_PARAMS="-s -k -b $COOKIE_JAR_FILE -c $COOKIE_JAR_FILE"

# Use netcat to scan port to check if the server is running
nc -z $IP $PORT
if [ "$?" = "1" ]; then
    echo "Server not running at $BASEURL"
    exit 1
fi

# If running on a UNB server, append my binaries folder to the path for programs like jq
HOSTNAME_REGEX=".*.cs.unb.ca"
if [[ $HOSTNAME =~ $HOSTNAME_REGEX ]]; then
    PATH="$PATH:/home1/ugrads/vmarica/bin"
fi

# Check if we have jq installed for formatting JSON data
JQ_INSTALLED=$(which jq > /dev/null; echo "$?")

PASSED_TEST_CASES=0
FAILED_TEST_CASES=0

# Error responses all have the the same format, so
# you can use this function to pretty-print them.
function print_error_response() {
    echo -ne "\tReason: "
    if [ "$JQ_INSTALLED" = "0" ]; then
        echo "$1" | jq ".message"
    else
        echo "$1"
    fi
}

function testcase() {
    title="$1"
    shift;
    EXPECTED_CODE="$1"
    shift;
    RESPONSE=$("$@" -w " CODE:%{http_code}")

    BODY=$(echo "$RESPONSE" | awk -F"CODE:" '{print $1}')
    CODE=$(echo "$RESPONSE" | awk -F"CODE:" '{print $2}' | xargs) # Use xargs to trim whitespace

    RESULT=" OK "
    COLOR=$(tput setaf 2 2>/dev/null)
    COLOR_RESET=$(tput sgr0 2>/dev/null)
    MSG=
    
    if [ $CODE != $EXPECTED_CODE ]; then
        RESULT="FAIL"
        COLOR=$(tput setaf 1 2>/dev/null)
        FAILED_TEST_CASES=$(($FAILED_TEST_CASES + 1))
    else
        PASSED_TEST_CASES=$(($PASSED_TEST_CASES + 1))
    fi

    echo -e "[${COLOR}${RESULT}${COLOR_RESET}] ${title}"
    if [ $CODE != $EXPECTED_CODE ]; then
        echo -e "\tExpected $EXPECTED_CODE but got $CODE"
        print_error_response "$BODY"
    fi
}

# Account creation tests
echo -e "\n== Local user creation =="
testcase "Missing username"     400 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"password": "xyz"}' $BASEURL/user
testcase "Missing password"     400 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "quintinity"}' $BASEURL/user
testcase "Valid credentials"    200 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "quintinity", "password": "xyz"}' $BASEURL/user
testcase "Duplicate username"   400 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "quintinity", "password": "xyz"}' $BASEURL/user

# Login/logout tests
echo -e "\n== Local user sessions =="
testcase "Logging in"  200 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "quintinity", "password": "xyz"}' $BASEURL/login
testcase "Logging out" 200 curl $CURL_PARAMS -X DELETE $BASEURL/login

echo -e "\n== LDAP user sessions =="
testcase "Logging in"  200 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "developer", "password": "abc123", "auth_type": "dev"}' $BASEURL/login
testcase "Logging" 200 curl $CURL_PARAMS -X DELETE $BASEURL/login

# Login and delete the account
echo -e "\n== Local user account deletion =="
curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "quintinity", "password": "xyz"}' $BASEURL/login
testcase "Delete account"  200 curl $CURL_PARAMS -X DELETE $BASEURL/user
testcase "Invalid session" 401 curl $CURL_PARAMS -X DELETE $BASEURL/user

# Login and delete the account
echo -e "\n== LDAP user account deletion =="
curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "developer", "password": "abc123", "auth_type": "dev"}' $BASEURL/login
testcase "Delete account"  200 curl $CURL_PARAMS -X DELETE $BASEURL/user
testcase "Invalid session" 401 curl $CURL_PARAMS -X DELETE $BASEURL/user

echo -e "\n$PASSED_TEST_CASES test(s) passed, $FAILED_TEST_CASES test(s) failed."

# Delete the cookie jar file
rm $COOKIE_JAR_FILE > /dev/null 2>&1

if [[ $FAILED_TEST_CASES -gt 0 ]]; then
    exit 1
fi
