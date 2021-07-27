FROM python:3.9

RUN mkdir -p /usr/src/meeting_scheduler
WORKDIR /usr/src/meeting_scheduler

ENV DATABASE_URI=${DATABASE_URI}
COPY . /usr/src/meeting_scheduler
RUN pip install -e .

EXPOSE 5000

CMD ["python", "meeting_scheduler/wsgi.py"]