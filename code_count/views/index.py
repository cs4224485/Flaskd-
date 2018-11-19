# Author: harry.cai
# DATE: 2018/9/2
from flask import Blueprint, request, render_template, session, redirect, jsonify
from ..utils import count
import json
from ..model import database
import zipfile
import os
import datetime
from ..model import *

main = Blueprint('main', __name__, )

BASEDIR = os.path.dirname(os.path.abspath('__file__'))


@main.before_request
def auth():
    user = session.get('user')
    if user:
        return None
    else:
        return redirect('/login')


@main.route('/index/', methods=['GET', 'POST'])
def index():
    user = session['user']
    data_list = database.fetch_all(
        'select username,counts,upload_date from CodeInfo inner join userinfo on CodeInfo.user_id=userinfo.nid')
    per_user_lines = database.fetch_all(
        'select sum(counts),username from CodeInfo inner join userinfo on CodeInfo.user_id=userinfo.nid group by user_id')

    per_user_data_list = []
    for item in per_user_lines:
        counts = int(item['sum(counts)'])
        per_user_data_list.append([item['username'], counts])

    print(per_user_data_list)
    is_chart = request.args.get('chart')
    print(is_chart)
    if is_chart:
        return jsonify({'date_list': per_user_data_list})
    return render_template('index.html', username=user['username'], nid=user['user_id'], data_list=data_list)


@main.route('/home/', methods=['GET', 'POST'])
def home():
    nid = session['user']['user_id']
    data_list = database.fetch_all(
        "select DISTINCT username,counts,upload_date from CodeInfo "
        "inner join userinfo "
        "on CodeInfo.user_id=userinfo.nid "
        "where userinfo.nid=%s", nid)
    date_list = []
    lines_list = []
    for item in data_list:
        date = datetime.datetime.strftime(item['upload_date'], '%Y-%m-%d')
        date_list.append(date)
        lines_list.append(item['counts'])
    is_chart = request.args.get('chart')
    if is_chart:
        return jsonify({'date_list': date_list, 'lines_list': lines_list})

    return render_template('home.html', data_list=data_list, date_list=date_list, username=session['user']['username'])


@main.route('/upload/<int:nid>', methods=['GET', 'POST'])
def load_file(nid):
    if request.method == 'GET':
        return render_template('upload.html')
    file_obj = request.files.get('code')
    file_name, file_type = file_obj.filename.rsplit('.', maxsplit=1)
    date = datetime.datetime.today().date()
    is_upload = database.fetch_one('select * from CodeInfo where upload_date=%s and user_id=%s', date, nid)
    if is_upload:
        return render_template('upload.html', msg='今日以已经上传')
    if file_type == 'zip':
        zip_file = zipfile.ZipFile(file_obj)
        import uuid
        ident_id = uuid.uuid4()
        file_path = os.path.join('files', str(ident_id), file_name)
        zip_file.extractall(file_path)
        ret = count.code_count(file_path)
        database.insert("insert into CodeInfo(counts,upload_date,user_id) values(%s,%s,%s)", ret, date, nid)

    return 'received'
