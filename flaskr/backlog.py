import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/backlog')

def add_type(form, db):
    type_name = form['type']
    type_in_db = db.execute(
        'SELECT id FROM backlog_types WHERE backlog_type = ?', (type_name,)
    ).fetchone()
    if not type_name:
        return jsonify(error='Type name is required!')
    if type_in_db is not None:
        return jsonify(error='Type name {} is already defined.'.format(type_name))
    db.execute(
        'INSERT INTO backlog_types (backlog_type) VALUES (?)', (type_name,)
    )
    db.commit()
    return jsonify(msg='Success!')

def get_all_types(db):
    all_types = db.execute(
        'SELECT * FROM backlog_types'
    ).fetchall()
    all_type_names = [row['backlog_type'] for row in all_types]
    return jsonify(types=all_type_names)


@bp.route('/type', methods=('GET', 'POST'))
def type_handler():
    db = get_db()
    if request.method == 'POST':
        return add_type(request.form, db)
    elif request.method == 'GET':
        return get_all_types(db)

def convert_backlog_row_to_json(row):
    return {
        'id': row['id'],
        'backlog_type': row['backlog_type'],
        'task_name': row['task_name'],
        'created': str(row['created']),
        'goal_date': str(row['goal_date'])
    }

def add_item(form, db):
    type_id = form['type_id']
    task_name = form['name']
    if not type_id:
        return jsonify(error='No type provided')
    elif not task_name:
        return jsonify(error='No task name provided')
    if not form.get('goal_date', None):
        db.execute(
            'INSERT INTO backlog (backlog_type, task_name) VALUES (?, ?)', 
            (type_id, task_name,)
        )
    else:
        goal_date = form['goal_date'] # temporary
        db.execute(
            'INSERT INTO backlog (backlog_type, task_name, goal_date) VALUES (?, ?, ?)', 
            (type_id, type_name, goal_date)
        )
    db.commit()
    return jsonify(msg='Success!')

def get_item(form, db):
    if not form.get('backlog_id', None):
        rows = db.execute(
            'SELECT * FROM backlog'
        ).fetchall()
        all_rows = []
        for row in rows:
            all_rows.append(convert_backlog_row_to_json(row))
        return jsonify(all_rows)
    id = request.form['backlog_id']
    row = db.execute(
        'SELECT * FROM backlog WHERE id = ?', (id,)
    ).fetchone()
    if row is None:
        return jsonify(error='No backlog matches that id!')
    return convert_backlog_row_to_json(row)

@bp.route('/item', methods=('GET', 'POST'))
def item_handler():
    db = get_db()
    if request.method == 'POST':
        return add_item(request.form, db)
    elif request.method == 'GET':
        return get_item(request.form, db)