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
            return jsonify(msg='Success!')
    elif request.method == 'GET':
        if type_in_db is None:
            error = 'Type name {} does not exist'.format(type_name)
        if error is None:
            print(type_in_db['id'])
            return jsonify(id=str(type_in_db['id']))
    return error
    # flash(error)

def convert_backlog_row_to_json(row):
    return jsonify(
        id=row['id'],
        backlog_type=row['backlog_type'],
        task_name=row['task_name'],
        created=row['created'],
        goal_date=row['goal_date']
    )

@bp.route('/item', methods=('GET', 'POST'))
def item():
    db = get_db()
    if request.method == 'POST':
        type_id = request.form['type_id']
        task_name = request.form['name']
        goal_date = None
        # goal_date = request.form['date']
        if not type_id:
            return jsonify(error='No type provided')
        elif not task_name:
            return jsonify(error='No task name provided')
        if not goal_date:
            db.execute(
                'INSERT INTO backlog (backlog_type, task_name) VALUES (?, ?)', 
                (type_id, task_name,)
            )
        else:
            db.execute(
                'INSERT INTO backlog (backlog_type, task_name, goal_date) VALUES (?, ?, ?)', 
                (type_id, type_name, goal_date)
            )
        db.commit()
        return jsonify(msg='Success!')
    # elif request.method == 'GET':
    else:
        id = request.form['backlog_id']
        if not id:
            return jsonify(error='No ID provided')
        row = db.execute(
            'SELECT * FROM backlog WHERE id = ?', (id,)
        ).fetchone()
        if row is None:
            return jsonify(error='No backlog matches that id!')
        return convert_backlog_row_to_json(row)