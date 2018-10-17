FROM debian:stretch-slim

# Install Python 3
RUN apt-get update && apt-get install python3 python3-pip

# Update Pip
RUN python3 -m pip install --upgrade pip

WORKDIR /app
COPY . .

RUN python3 -m pip install -r requirements.txt


