from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
# from db_connect import create_connection
from contextlib import closing
from datetime import datetime
from user import user
from website import website
from admin import admin
from flask_compress import Compress
from datetime import timedelta

now = datetime.now()

app = Flask(__name__)
app.secret_key = secrets.token_hex(1000)
app.permanent_session_lifetime = timedelta(minutes=15)

# Register blueprints
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(website)

Compress(app)


@app.context_processor
def utility_processor():
    return dict(url_for=url_for)


@app.context_processor
def inject_global_template_vars():
    msg = session.pop('message', None)
    return dict(message=msg)


@app.context_processor
def inject_current_datetime():
    return {
        'current_datetime': now.strftime("%B %d, %Y %I:%M %p")
    }


# if __name__ == '__main__':
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
