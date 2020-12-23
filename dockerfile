FROM python:3.9.1-alpine

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ .
ENV FLASK_APP=app.py

CMD flask run -h 0.0.0.0 -p 5000