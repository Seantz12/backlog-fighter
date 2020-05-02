import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/backlog')

@bp.route('/type', methods=('GET', 'POST'))
def add_type():
    type_name = request.form['type']
    db = get_db()
    error = None
    if not type_name:
        error = 'Type name is required'
    type_in_db = db.execute(
        'SELECT id FROM backlog_types WHERE backlog_type = ?', (type_name,)
    ).fetchone()
    if request.method == 'POST':
        if type_in_db is not None:
            error = 'Type name {} is already defined'.format(type_name)
        if error is None:
            db.execute(
                'INSERT INTO backlog_types (backlog_type) VALUES (?)', (type_name,)
            )
            db.commit()
            return 'Success!'
    elif request.method == 'GET':
        if type_in_db is None:
            error = 'Type name {} does not exist'.format(type_name)
        if error is None:
            print(type_in_db['id'])
            return jsonify(str(type_in_db['id']))
    return error
    # flash(error)

