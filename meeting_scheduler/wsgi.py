import os

import msal
from flask import redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from flask_session import Session
from flask_talisman import Talisman
from google_secrets_manager_client.secrets_manager import init_secret_manager
from outlook_calendar_service.calendar_api import get_user

from meeting_scheduler.app_config import Settings
from meeting_scheduler.src import app_factory

settings = Settings()
app = app_factory.get_app()
app.config.from_object(settings)
Session(app)
migrate = Migrate(app, app_factory.get_db())


@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"])


@app.route("/login")
def login():
    session["flow"] = _build_auth_code_flow(scopes=settings.scope)
    return render_template(
        "login.html",
        auth_url=session["flow"]["auth_uri"],
    )


@app.route(settings.redirect_path)
def authorized():
    try:
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        # print(result.get("id_token_claims").get("preferred_username"))
        # print(result.get("refresh_token"))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    except ValueError:
        pass
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        settings.outlook_authority + "/oauth2/v2.0/logout"
        "?post_logout_redirect_uri=" + url_for("index", _external=True))


@app.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(settings.scope)
    if not token:
        return redirect(url_for("login"))
    graph_data = get_user(token)
    return render_template('display.html', result=graph_data)


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


if __name__ == '__main__':
    if "DYNO" in os.environ:
        init_secret_manager()
        Talisman(app)
        app.run(host="0.0.0.0", port=int(os.getenv('PORT', 5000)))
    else:
        app.run(port=int(os.getenv('PORT', 5000)), debug=True)
