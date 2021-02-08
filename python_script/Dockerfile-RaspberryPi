FROM homeassistant/armv7-base-debian:latest

WORKDIR .
COPY . .

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install <YOUR_PACKAGE_1>
RUN pip3 install <YOUR_PACKAGE_2>
