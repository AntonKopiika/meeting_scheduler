FROM python:3.9

WORKDIR /usr/src/meeting_scheduler
COPY . /usr/src/meeting_scheduler
RUN pip install -e .

EXPOSE 5000
RUN celery -A async_task.tasks worker -l INFO
RUN celery -A async_task.tasks beat
CMD ["python", "meeting_scheduler/wsgi.py"]