FROM debian:stretch-slim

# Install Python 3
RUN apt-get update && \
    apt-get install python3

# Ensure we have pip
RUN python3 -m ensurepip

# Install required packages
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install "Flask==0.12.2" "PyMySQL==0.7.11"

WORKDIR /app
COPY ./src .

