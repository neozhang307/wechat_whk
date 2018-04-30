from __future__ import absolute_import, unicode_literals
import os
from flask import Flask, request, abort, render_template

from message import message
from sqlite_helper import SQLiteHelper
from hwk_helper import HomeworkHelper
from time_helpter import timestamp2date
import sys
# set token or get from environments
from util import *

app = Flask(__name__)


@app.route('/')
def index():
    host = request.url_root
    return render_template('index.html', host=host)
 #   return "hello world"

@app.route('/name/<name>')
def showname(name):
    return "hello" + name

@app.route('/homework/<date>')
def showhomework(date):
    hwker = HomeworkHelper(date)
    user_d, user_d_rev = get_userlist()
    homework = {user_d[uid]:hwker.get(uid) for uid in range(501,518)}
    return render_template("show_dict.html", result=homework)

@app.route('/checkwork/<date>')
def checkwork(date):
    hwker = HomeworkHelper(date)
    user_d, user_d_rev = get_userlist()
    delayed = hwker.checkunsubmit(user_d.keys())
    name = [user_d[id] for id in delayed]
    return render_template("show_list.html", data=name)

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
