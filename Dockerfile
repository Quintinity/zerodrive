FROM debian:stretch-slim

# Install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip libffi-dev

# Update Pip
RUN python3 -m pip install --upgrade pip

WORKDIR /app
COPY ./server .
COPY ./client/dist ./static

ENV ZERODRIVE_SERVER_STATIC_FILE_DIR=./static
ENV ZERODRIVE_SERVER_CERT_FILE=/certs/cert.pem
ENV ZERODRIVE_SERVER_KEY_FILE=/certs/key.pem
ENV ZERODRIVE_SERVER_HOST=0.0.0.0

RUN python3 -m pip install -r requirements.txt

CMD python3 app.py
