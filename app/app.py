from flask import Flask, Response, json, Blueprint, render_template
from migration.controllers import migration
from collect.controllers import collect
from status.controllers import status
from dumping.controllers import dumping
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from flask_cors import CORS
import os
import logging
import sentry_sdk

app = Flask(__name__, template_folder='web')
CORS(app)

# Sentry
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    integrations=[FlaskIntegration()]
)

# WEB
@app.route('/')
def index():
    return render_template("index.html")


# MODULES
app.register_blueprint(migration, url_prefix="/api/migration")
app.register_blueprint(collect, url_prefix="/api/collect")
app.register_blueprint(status, url_prefix="/api/status")
app.register_blueprint(dumping, url_prefix="/api/dumping")

# Handling 403
@app.errorhandler(403)
def handler_not_found(error):
    data = json.dumps({"message": "Forbidden!"})
    return Response(data, status=403, mimetype="application/json")


# Handling 404
@app.errorhandler(404)
def handler_not_found(error):
    data = json.dumps({"message": "Not found!"})
    return Response(data, status=404, mimetype="application/json")


# Handling 405
@app.errorhandler(405)
def handler_not_found(error):
    data = json.dumps({"message": "Not allowed!"})
    return Response(data, status=405, mimetype="application/json")


# Handling 500
@app.errorhandler(500)
def handler_not_found(error):
    data = json.dumps({"message": "Internal server error!"})
    return Response(data, status=500, mimetype="application/json")


# ENV
debug = os.environ["APP_DEBUG"]
host = os.environ["APP_HOST"]
port = os.environ["APP_PORT"]

# RUN
app.run(debug=debug, host=host, port=port)
