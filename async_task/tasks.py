from celery import Celery
from meeting_scheduler.src import app_factory
from meeting_scheduler.src.models import UserAccount

from meeting_scheduler.app_config import Settings
from outlook_calendar_service.calendar_api import sync_meetings_with_db

celery = Celery('tasks',
             broker=Settings().celery_broker_url,
             backend=Settings().celery_backend_url)


@celery.task
def sync_all_outlook_calendar_users():
    app = app_factory.get_app()
    with app.app_context():
        accounts = UserAccount.query.filter_by(provider="outlook").all()
        for account in accounts:
            sync_outlook_user.delay(account.id)


@celery.task
def sync_outlook_user(account_id: int):
    app = app_factory.get_app()
    with app.app_context():
        sync_meetings_with_db(account_id)


celery.conf.beat_schedule = {
    'sync-user-meetings-300-seconds': {
        'task': 'async_task.tasks.sync_all_outlook_calendar_users',
        'schedule': 300.0,
        'args': ()
    },
}
celery.conf.timezone = 'UTC'