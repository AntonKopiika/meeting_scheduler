import http
import os
from datetime import datetime, timedelta

import msal
import requests
from dateutil.relativedelta import relativedelta
from flask import flash, redirect, render_template, request, session, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from flask_session import Session
from flask_talisman import Talisman
from google_secrets_manager_client.encryption import CryptoService
from google_secrets_manager_client.secrets_manager import init_secret_manager
from outlook_calendar_service.calendar_api import OutlookApiService
from werkzeug.urls import url_parse

from meeting_scheduler.app_config import Settings
from meeting_scheduler.src import app_factory
from meeting_scheduler.src.db_service import create_user_account
from meeting_scheduler.src.forms.event import EventForm
from meeting_scheduler.src.forms.login import LoginForm
from meeting_scheduler.src.forms.meeting import MeetingForm
from meeting_scheduler.src.models import User

settings = Settings()
app = app_factory.get_app()
app.config.from_object(settings)
Session(app)
CORS(app)
jwt = JWTManager(app)
migrate = Migrate(app, app_factory.get_db())
login_manager = LoginManager()
login_manager.init_app(app)


@login_required
@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    token = _get_token_from_cache(settings.scope)
    if not token:
        return redirect(url_for("auth_login"))
    form = EventForm()
    if form.validate_on_submit():
        title = form.title.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        duration = form.duration.data
        working_days = form.working_days.data
        description = form.description.data
        event_type = form.event_type.data
        datetime_format = Settings().datetime_format
        start_time = datetime.combine(start_date, form.start_time.data).strftime(datetime_format)
        end_time = datetime.combine(end_date, form.end_time.data).strftime(datetime_format)
        data = {
            "host": current_user.id,
            'title': title,
            'start_date': str(start_date),
            'end_date': str(end_date),
            'duration': duration,
            'working_days': working_days,
            'description': description,
            'event_type': event_type,
            "start_time": start_time,
            "end_time": end_time
        }
        response = requests.post("http://127.0.0.1:5000/event", json=data)
        if response.status_code == http.HTTPStatus.CREATED:
            flash("New event successfully created")
            return redirect("index")
        else:
            flash("Something went wrong while creating new event")
    return render_template('create_event.html', form=form)


@app.route("/auth_login")
def auth_login():
    session["flow"] = _build_auth_code_flow(scopes=settings.scope)
    return redirect(session["flow"]["auth_uri"])


@app.route(settings.redirect_path)
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        email = result.get("id_token_claims").get("preferred_username")
        refresh_token = result.get("refresh_token")
        create_user_account(
            email,
            refresh_token,
            current_user,
            "outlook",
            "refresh_token"
        )
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:
        pass
    return redirect("http://127.0.0.1:3000/about")


@app.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("index"))


@app.route("/auth_logout")
def auth_logout():
    session.clear()
    return redirect(
        settings.outlook_authority + "/oauth2/v2.0/logout"
                                     "?post_logout_redirect_uri=" + url_for("index", _external=True))


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        settings.outlook_client_id, authority=authority or settings.outlook_authority,
        client_credential=settings.outlook_client_secret, token_cache=cache)


def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=settings.redirect_uri)


def _get_token_from_cache(scope=None):
    cache = _load_cache()
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


def _get_token_from_refresh_token(user: User):
    cache = _load_cache()
    cca = _build_msal_app(cache=cache)
    cred = CryptoService().decrypt(user.accounts[0].cred)
    result = cca.acquire_token_by_refresh_token(
        refresh_token=cred, scopes=settings.scope)
    _save_cache(cache)
    return result


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    if "DYNO" in os.environ:
        init_secret_manager()
        Talisman(app)
        app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
    else:
        app.run(port=int(os.getenv('PORT', 5000)), debug=True)
