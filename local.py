from __future__ import absolute_import, unicode_literals
import os
from flask import Flask, request, abort, render_template, redirect

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

@app.route('/showhomework/<date>')
def showhomework(date):
    hwker = HomeworkHelper(date)
    user_d, user_d_rev = get_userlist()
    homework = {user_d[uid]:hwker.get(uid) for uid in range(501,518)}
    unsubmit = 0;
    submit = len(homework)
    for data in homework.values():
        if(len(data)==0):
            unsubmit+=1
            submit-=1
    return render_template("/mobile/show_dict.html",date=date, result=homework,submit=submit,unsubmit=unsubmit)

@app.route('/homework/')
def homeworkform():
    return render_template('/mobile/form.html',date="20180501")

@app.route('/homework/',methods=['POST'])
def homework():
    text = request.form['text'] 
    if("hito" in request.form.keys()):
        return redirect('/showcheckresult/'+text,code=302)
    if("keka" in request.form.keys()):
        return redirect('/showhomework/'+text,code=302)

@app.route('/showcheckresult/<date>')
def showcheckresult(date):
    hwker = HomeworkHelper(date)
    user_d, user_d_rev = get_userlist()
    delayed = hwker.checkunsubmit(user_d.keys())
    name = [user_d[id] for id in delayed]
    return render_template("/mobile/show_list.html", data=name,date=date)

@app.route('/checkwork/')
def checkworkform():
    return render_template('my-form.html')

@app.route('/checkwork/',methods=['POST'])
def checkwork():
    text = request.form['text'] 
    return redirect('/showcheckresult/'+text,code=302)

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
