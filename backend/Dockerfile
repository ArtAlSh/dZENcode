FROM python:3.10-slim-buster

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install build-essential python3-dev libpq-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

RUN mkdir media
RUN python3 manage.py makemigrations

CMD /bin/sh -c "python3 manage.py migrate && daphne config.asgi:application -b 0.0.0.0 -p 8000"
EXPOSE 8000
