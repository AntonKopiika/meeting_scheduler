FROM python:3.9

WORKDIR /usr/src/meeting_scheduler
COPY . /usr/src/meeting_scheduler
RUN pip install -e .

EXPOSE 5000

CMD ["python", "meeting_scheduler/wsgi.py"]