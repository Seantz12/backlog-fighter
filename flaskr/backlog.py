import functools

from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, jsonify
)

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/backlog')

def get_types(form, db):
    all_types = db.execute(
        'SELECT DISTINCT backlog_type FROM backlog'
    ).fetchall()
    all_type_names = [row['backlog_type'] for row in all_types]
    return jsonify(types=all_type_names)


@bp.route('/type', methods=('GET', 'POST'))
def type_handler():
    db = get_db()
    if request.method == 'GET':
        return get_types(request.form, db)
    else:
        return jsonify(error='Invalid request type')

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
        goal_date = form['goal_date']
        db.execute(
            'INSERT INTO backlog (backlog_type, task_name, goal_date) VALUES (?, ?, ?)', 
            (type_id, type_name, goal_date)
        )
    db.commit()
    return jsonify(msg='Success!')


# remember to validate form input
def get_item(form, db):
    column = request.args.get('column', default='id', type=str)
    ascending = request.args.get('ascending', default='true', type=str)
    order = 'ASC' if  ascending == 'true' else 'DESC'
    where_clause = ''
    search_filter = request.args.get('search', default='', type=str)
    types = request.args.get('types', default='', type=str)
    if search_filter != '':
        where_clause = "WHERE task_name LIKE '{}%'".format(search_filter)
        if types != '':
            where_clause += " AND ("
            type_array = types.split(',')
            for type_filter in type_array:
                where_clause += "backlog_type = '{}' OR".format(type_filter)
            where_clause = where_clause[:-3] + ')'
    elif types != '':
        where_clause = "WHERE "
        type_array = types.split(',')
        for type_filter in type_array: 
            where_clause += "backlog_type = '{}' OR ".format(type_filter)
        where_clause = where_clause[:-3]
    rows = db.execute(
        'SELECT * FROM backlog {} ORDER BY {} {}'.format(
            where_clause, column, order)
    ).fetchall()
    all_rows = []
    for row in rows:
        all_rows.append(convert_backlog_row_to_json(row))
    return jsonify(all_rows)

@bp.route('/item', methods=('GET', 'POST'))
def item_handler():
    db = get_db()
    if request.method == 'POST':
        return add_item(request.form, db)
    elif request.method == 'GET':
        print("hi")
        return get_item(request.form, db)
    else:
        return jsonify(error='Invalid request type')