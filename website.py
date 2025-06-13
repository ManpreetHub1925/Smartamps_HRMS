from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from contextlib import closing
from datetime import datetime
from urllib.parse import urlencode
import json
from sqlalchemy import text
# from db_connect import engine
from flask import current_app
import re

website = Blueprint('website', __name__)


@website.route('/')
def index():
    return render_template(
        'website/index.html'
    )

