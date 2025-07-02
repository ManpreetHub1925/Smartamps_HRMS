from flask import Flask, jsonify, request, render_template, redirect, url_for, session
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
import secrets
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from codes.db.db import create_connections

engine = create_connections()

load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(16))

"""Register Flask blueprints"""
from codes.admin.admin import admin
from codes.frontend.website import website_bp
from codes.user.user import user
from codes.auth.auth import auth
from codes.superadmin.superadmin import superadmin
from codes.routes.routes import routes
from codes.administration.setting import setting

app.register_blueprint(admin)
app.register_blueprint(website_bp)
app.register_blueprint(user)
app.register_blueprint(auth)
app.register_blueprint(superadmin)
app.register_blueprint(routes)
app.register_blueprint(setting)



if __name__ == '__main__':
    debug_mode = os.getenv("APP_DEBUG", "True").lower() == "true"
    app.run(
        debug=debug_mode,
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", "5000"))
    )

