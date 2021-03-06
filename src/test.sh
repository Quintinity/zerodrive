#!/bin/bash

HOST="${ZERODRIVE_SERVER_HOST:-127.0.0.1}"
PORT="${ZERODRIVE_SERVER_PORT:-40500}"
BASEURL=https://$HOST:$PORT

echo -e "Running tests on $BASEURL"

COOKIE_JAR_FILE="cookiejar.bin"
CURL_PARAMS="-s -k -b $COOKIE_JAR_FILE -c $COOKIE_JAR_FILE"

# Use netcat to scan port to check if the server is running
nc -z $HOST $PORT
if [ "$?" = "1" ]; then
    echo "Server not running at $BASEURL"
    exit 1
fi

# If running on a UNB CS server, append my binaries folder to the path for programs like jq
UNB_HOSTNAME_REGEX=".*.cs.unb.ca"
if [[ $HOSTNAME =~ $UNB_HOSTNAME_REGEX ]]; then
    PATH="/home1/ugrads/vmarica/bin:$PATH"
fi

# Check if we have jq installed for parsing JSON data
JQ_INSTALLED=$(which jq > /dev/null; echo "$?")
if [ "$JQ_INSTALLED" != "0" ]; then
    echo "Cannot find 'jq'! Please ensure it is available in the PATH."
    exit 1
fi

PASSED_TEST_CASES=0
FAILED_TEST_CASES=0

LDAP_USERNAME=developer
LDAP_PASSWORD=abc123

# Error responses all have the the same format, so
# you can use this function to pretty-print them.
function print_error_response() {
    echo -ne "\tReason: "
    echo "$1" | jq ".message"
}

function testcase() {
    local title="$1"
    shift;
    local EXPECTED_CODE="$1"
    shift;
    RESPONSE=$("$@" -w " CODE:%{http_code}")

    BODY=$(echo "$RESPONSE" | awk -F"CODE:" '{print $1}')
    CODE=$(echo "$RESPONSE" | awk -F"CODE:" '{print $2}' | xargs) # Use xargs to trim whitespace

    local RESULT=" OK "
    local COLOR=$(tput setaf 2 2>/dev/null)
    local COLOR_RESET=$(tput sgr0 2>/dev/null)
    local MSG=
    
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
testcase "Try logging in when already logged in" 400 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "quintinity", "password": "xyz"}' $BASEURL/login
testcase "Logging out" 200 curl $CURL_PARAMS -X DELETE $BASEURL/login

echo -e "\n== LDAP user sessions =="
testcase "Logging in"  200 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d "{\"username\": \"$LDAP_USERNAME\", \"password\": \"$LDAP_PASSWORD\", \"auth_type\": \"dev\"}" $BASEURL/login
testcase "Try logging in when already logged in" 400 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d "{\"username\": \"$LDAP_USERNAME\", \"password\": \"$LDAP_PASSWORD\", \"auth_type\": \"dev\"}" $BASEURL/login
testcase "Logging out" 200 curl $CURL_PARAMS -X DELETE $BASEURL/login

# Test getting user data
echo -e "\n== User data =="
curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d "{\"username\": \"$LDAP_USERNAME\", \"password\": \"$LDAP_PASSWORD\", \"auth_type\": \"dev\"}" $BASEURL/login
testcase "Get current user's data" 200 curl $CURL_PARAMS -H "Content-Type: application/json" -X GET $BASEURL/user
ROOT_FOLDER_ID=$(echo "$BODY" | jq .root_folder_id)

# Test creating, updating, and deleting folders
echo -e "\n== Folders =="
testcase "Create a folder" 200 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d "{\"name\": \"Folder1\", \"parent_folder_id\": \"$ROOT_FOLDER_ID\"}" $BASEURL/folder

NEW_FOLDER_ID=$(echo "$BODY" | jq .new_folder_id)
testcase "Try to create folder with duplicate name" 400 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d "{\"name\": \"Folder1\", \"parent_folder_id\": \"$ROOT_FOLDER_ID\"}" $BASEURL/folder
testcase "Try to create folder under non-existent folder" 404 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"name": "Folder1", "parent_folder_id": "-1"}' $BASEURL/folder
curl $CURL_PARAMS -X DELETE $BASEURL/login
curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "quintinity", "password": "xyz"}' $BASEURL/login
testcase "Try to create folder under another user's folder" 401 curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d "{\"name\": \"Folder2\", \"parent_folder_id\": \"$ROOT_FOLDER_ID\"}" $BASEURL/folder
curl $CURL_PARAMS -X DELETE $BASEURL/login
curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d "{\"username\": \"$LDAP_USERNAME\", \"password\": \"$LDAP_PASSWORD\", \"auth_type\": \"dev\"}" $BASEURL/login

testcase "Rename a folder" 200 curl $CURL_PARAMS -H "Content-Type: application/json" -X PUT -d '{"name": "Folder10"}' $BASEURL/folder/$NEW_FOLDER_ID
testcase "Try to rename a folder that doesn't exist" 404 curl $CURL_PARAMS -H "Content-Type: application/json" -X PUT -d '{"name": "Folder10"}' $BASEURL/folder/0

testcase "Get folder info" 200 curl $CURL_PARAMS -X GET $BASEURL/folder/$NEW_FOLDER_ID
testcase "Try to get info from a folder that doesn't exist" 404 curl $CURL_PARAMS -X GET $BASEURL/folder/0

testcase "Delete a folder" 200 curl $CURL_PARAMS -X DELETE $BASEURL/folder/$NEW_FOLDER_ID
testcase "Try to delete a folder that doesn't exist" 404 curl $CURL_PARAMS -X DELETE $BASEURL/folder/0
testcase "Try to delete a root folder" 401 curl $CURL_PARAMS -X DELETE $BASEURL/folder/$ROOT_FOLDER_ID

# Test file upload, download, renaming, and deletion
echo -e "\n== Files =="
DUMMY_FILE="testfile.txt"
echo "Hello, world!" > $DUMMY_FILE
testcase "Upload a file" 200 curl $CURL_PARAMS -F "parent_folder=$ROOT_FOLDER_ID" -F "file=@$DUMMY_FILE" $BASEURL/file
NEW_FILE_ID=$(echo $BODY | jq .new_file_id)
testcase "Upload a duplicate file" 403 curl $CURL_PARAMS -F "parent_folder=$ROOT_FOLDER_ID" -F "file=@$DUMMY_FILE" $BASEURL/file
testcase "Try to upload a file to a folder that doesn't exist" 404 curl $CURL_PARAMS -F "parent_folder=0" -F "file=@$DUMMY_FILE" $BASEURL/file

testcase "Download a file" 200 curl $CURL_PARAMS -X GET $BASEURL/file/$NEW_FILE_ID
testcase "Try to download a file that doesn't exist" 404 curl $CURL_PARAMS -X GET $BASEURL/file/0

testcase "Rename a file" 200 curl $CURL_PARAMS -X PUT -H "Content-Type: application/json" -d '{"new_file_name": "somefile.txt"}' $BASEURL/file/$NEW_FILE_ID
testcase "Try to rename a file that doesn't exist" 404 curl $CURL_PARAMS -X PUT -H "Content-Type: application/json" -d '{"new_file_name": "somefile.txt"}' $BASEURL/file/0

testcase "Delete a file" 200 curl $CURL_PARAMS -X DELETE $BASEURL/file/$NEW_FILE_ID
testcase "Try to delete a file that doesn't exist" 404 curl $CURL_PARAMS -X DELETE $BASEURL/file/$NEW_FILE_ID

rm $DUMMY_FILE

# Login and delete the account
echo -e "\n== LDAP user account deletion =="
testcase "Delete account"  200 curl $CURL_PARAMS -X DELETE $BASEURL/user
testcase "Invalid session" 400 curl $CURL_PARAMS -X DELETE $BASEURL/user

# Login and delete the account
echo -e "\n== Local user account deletion =="
curl $CURL_PARAMS -H "Content-Type: application/json" -X POST -d '{"username": "quintinity", "password": "xyz"}' $BASEURL/login
testcase "Delete account"  200 curl $CURL_PARAMS -X DELETE $BASEURL/user
testcase "Invalid session" 400 curl $CURL_PARAMS -X DELETE $BASEURL/user

echo -e "\n$PASSED_TEST_CASES test(s) passed, $FAILED_TEST_CASES test(s) failed."

# Delete the cookie jar file
rm $COOKIE_JAR_FILE > /dev/null 2>&1

if [[ $FAILED_TEST_CASES -gt 0 ]]; then
    exit 1
fi
