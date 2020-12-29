FROM ubuntu:18.04
MAINTAINER John Else <john.else@gmail.com>

RUN apt-get update
RUN apt-get -y install lighttpd
RUN apt-get install -y python3-pip python3-dev

ENV LIGHTTPD_VERSION=1.4.55-r1

RUN apt-get install lighttpd -y

COPY ./etc/lighttpd/* /etc/lighttpd/


EXPOSE 80

WORKDIR /var/www/shippingchallenge

COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./ .

CMD ["lighttpd","-D","-f","/etc/lighttpd/lighttpd.conf"]