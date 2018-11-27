FROM debian:stretch-slim

# Install Python 3
RUN apt-get update && apt-get install python3 python3-pip

# Update Pip
RUN python3 -m pip install --upgrade pip

WORKDIR /app
COPY ./server .
COPY ./client/dist ./static

ENV ZERODRIVE_SERVER_STATIC_FILE_DIR=./static
ENV ZERODRIVE_CERT_FILE=/certs/cert.pem
ENV ZERODRIVE_KEY_FILE=/certs/key.pem

RUN python3 -m pip install -r requirements.txt

CMD python3 app.py
