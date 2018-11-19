# Author: harry.cai
# DATE: 2018/9/5
from flask import Blueprint, request, render_template,session,redirect
from ..model import database
authenticate = Blueprint('auth', __name__,)


@authenticate.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user_obj = database.fetch_one('select * from userinfo where username=%s and password=%s', username,password)
        if user_obj:
            session['user'] = {'username': user_obj['username'],
                               'user_id': user_obj['nid'],
                               'nickname': user_obj['nickname']}
            return redirect('/index')
    return render_template('sign_in.html')