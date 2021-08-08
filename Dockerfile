FROM python:3.9

RUN mkdir -p /usr/src/meeting_scheduler
WORKDIR /usr/src/meeting_scheduler

ENV DATABASE_URI postgresql://fthsbvaxhvjxhr:08a47f5b1894df0372b2a5deccdc9ff6fc696c0b92b68f6e742ca672a22c8417@ec2-54-155-87-214.eu-west-1.compute.amazonaws.com:5432/dbm8lvoo16kvg
ENV OUTLOOK_APP_SECRET dQb2BbHyW3..632L7tDb.9j8a1-gi57e6L
COPY . /usr/src/meeting_scheduler
RUN pip install -e .

EXPOSE 5000

CMD ["python", "meeting_scheduler/wsgi.py"]