
from flask import Blueprint, render_template, redirect, url_for, session, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from contextlib import closing
from datetime import datetime
from urllib.parse import urlencode
import json
from sqlalchemy import text
from codes.db.db import create_connections
from flask import current_app
import re
from functools import wraps
import os
import dotenv

engine = create_connections()


api = Blueprint('api', __name__)


def get_user_details(employee_code):
    with engine.connect() as conn:
        query = text("""
            SELECT * FROM v_employee_profile 
            WHERE employee_code = :employee_code AND user_is_active = 1
        """)
        result = conn.execute(query, {'employee_code': employee_code}).mappings().fetchone()
    return result



@api.route('/api/punch', methods=['POST'])
def receive_punch():
    token = request.headers.get('Authorization')
    if token != f"Bearer {os.getenv("SECRET_KEY", secrets.token_hex(16))}":
        return jsonify({'status': 'unauthorized'}), 401
    try:
        data = request.json

        # Basic validation
        required_fields = ['employee_id', 'timestamp', 'status', 'device_id']
        if not all(field in data for field in required_fields):
            return jsonify({'status': 'error', 'message': 'Missing fields'}), 400

        employee_id = data['employee_id']
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')  # ISO format
        status = data['status'].upper()
        device_id = data['device_id']

        if status not in ['IN', 'OUT']:
            return jsonify({'status': 'error', 'message': 'Invalid status'}), 400

        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO attendance (employee_id, punch_time, status, device_id)
                VALUES (:employee_id, :punch_time, :status, :device_id)
            """), {
                'employee_id': employee_id,
                'punch_time': timestamp,
                'status': status,
                'device_id': device_id
            })

        return jsonify({'status': 'success'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


