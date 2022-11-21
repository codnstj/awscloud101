import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from psycopg2 import connect
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://1ec8bc09682e478695b180119159a056@o4504179022692352.ingest.sentry.io/4504194406023168",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

dir = os.path.dirname(__file__)
with open(os.path.join(dir, 'db_credentials')) as data:
    db_credentials = json.load(data)

@app.route("/")
def index():
    conn = connect(
        dbname='postgres',
        user=db_credentials['username'],
        host=db_credentials['host'],
        password=db_credentials['password']
    )
    conn.close()
    return """
        <style>body {background-color: green}</style>
        <h1 style='color:black'>Everything is working fine</h1>
    """

@app.route("/error/")
def error():
    conn = connect(
        dbname='postgres',
        user=db_credentials['username'],
        host=db_credentials['host'],
        password='asdf1234'
    )
    division_by_zero = 1 / 0
