from __future__ import absolute_import, unicode_literals
import os
from flask import Flask, request, abort, render_template, redirect
from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException

from message import message,split_msg
from sqlite_helper import SQLiteHelper
from hwk_helper import HomeworkHelper
from scbun_helper import BunHelper
from sethwk_helper import SetHomeworkHelper
import sys
# set token or get from environments
TOKEN = os.getenv('WECHAT_TOKEN', 'imneo')
EncodingAESKey = os.getenv('WECHAT_ENCODING_AES_KEY', '1wGqo5kzdHNETfD56xqsN7WNP9TBBIMZDogPdKxTIYb')
AppId = os.getenv('WECHAT_APP_ID', 'wxb580d81e415849e1')

app = Flask(__name__)


#@app.route('/')
def index():
    host = request.url_root
 #   return render_template('index.html', host=host)
    #return "hello world"
    return redirect('/homework/',code=302)

from util import *
@app.route('/showhomework/<date>')
def showhomework(date):
    hwker = BunHelper(date)
    user_d, user_d_rev = get_userlist()
    
    unsubmit = len(user_d);
    submit = 0;
    
    if hwker.is_ext()==1:
        homework = {user_d[uid]:hwker.get(uid) for uid in range(501,518)}
        for data in homework.values():
            if(len(data)!=0):
                unsubmit-=1
                submit+=1
    else:
        homework = {user_d[uid]:"" for uid in range(501,518)}
    return render_template("/mobile/show_dict.html",date=date, result=homework,submit=submit,unsubmit=unsubmit)

@app.route('/showhomework2/<date>')
def showhomework2(date):
    hwker = BunHelper(date)
    user_d, user_d_rev = get_userlist()
    if hwker.is_ext()==1:
        homework = {user_d[uid]:hwker.get(uid) for uid in range(501,518)}
    else:
        homework = {user_d[uid]:"" for uid in range(501,518)}
    return render_template("/show_dict.html",date=date, result=homework)

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

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    encrypt_type = request.args.get('encrypt_type', '')
    msg_signature = request.args.get('msg_signature', '')

    print('signature:', signature, file=sys.stderr)
    print('timestamp: ', timestamp, file=sys.stderr)
    print('nonce:', nonce, file=sys.stderr)
    print('echo_str:', echo_str, file=sys.stderr)
    print('encrypt_type:', encrypt_type, file=sys.stderr)
    print('msg_signature:', msg_signature, file=sys.stderr)

    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        return echo_str
    else:
        print('Raw message: \n%s' % request.data)
        crypto = WeChatCrypto(TOKEN, EncodingAESKey, AppId)
        try:
            msg = crypto.decrypt_message(
                request.data,
                msg_signature,
                timestamp,
                nonce
            )
            print('Descypted message: \n%s' % msg)
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        msg = parse_message(msg)
        if msg.type == 'text':
            cmsg = message()
            psdmsg, cid = cmsg.msg_mng(msg.content)
            appuserid=msg.source
            content=SQLiteHelper()
            codes=content.get(appuserid)
            print("psdmsg is "+psdmsg)
            known_user=0
            if 'name_id' in codes.keys():
                known_user=1
            if(known_user!=1 and(cid!=2 or cid!=3)):
                reply = create_reply(get_text('uninituser')+get_text('illustrate'),msg)
            if cid==1:
               #submit homework 
                if len(psdmsg)>4:
                    nameid = codes['name_id']
                    user_d,user_d_rev = get_all_userlist()
                    name = user_d[nameid]
                    hwk = HomeworkHelper(msg.create_time.strftime("%Y%m%d"))
                    hwk.set(nameid,psdmsg)
                    reply = create_reply(name+get_text('namago')+get_text('gothwk'),msg)
                else:
                    reply = create_reply("should longer than 0",msg)
            elif cid==2 or cid==3:
                #updatename
                user_d,user_d_rev = get_all_userlist()
                name,errcode = check_existence(psdmsg,user_d)
                if errcode==1:
                    codes.update({'name':name})
                    codes.update({'name_id':user_d_rev[name]})
                    content.set(appuserid,codes)
                    if user_d_rev[name]==0:
                        reply = create_reply(name+"先生"+get_text('thx'),msg)
                    else:
                        reply = create_reply(name+get_text('namago')+get_text('thx'),msg)
                else:
                    reply = create_reply(name+'さんは'+get_text('uninituser')+get_text('gethelp'),msg)
            elif cid==4:
                hwk = SetHomeworkHelper()
                mhk = hwk.get(msg.create_time.strftime("%Y%m%d"))
                if(len(mhk)==0):
                    reply = create_reply(get_text("nohomework"),msg)
                else:
                    reply = create_reply(mhk,msg)
                    
                    
            elif cid==5:#get sakubun in specific date
                date = psdmsg
                hwker = BunHelper(date)
                
                if hwker.is_ext()==1:
                    if len(hwker.get(codes['name_id']))!=0:
                        reply = create_reply(hwker.get(codes['name_id']),msg)
                    else:
                        reply = create_reply("unsubmit",msg)
                else:
                    reply = create_reply(get_text("nobun"),msg)
            elif cid==6:#modify sakubun
                date, nbun, errid = split_msg(psdmsg)
                print("date"+date)
                print("bun"+nbun)
                if(errid!=1):
                    reply = create_reply("formaterror",msg)
                else:
                    hwker = BunHelper(date)
                    if hwker.is_ext()==1:
                        pre = hwker.get(codes['name_id'])
                        hwker.set(codes['name_id'],nbun)
                        reply = create_reply("change \""+pre+"\" to \""+nbun+"\"",msg)
                    else:
                        reply = create_reply(get_text("nobun"),msg)
                
            elif cid==8:
                reply = create_reply(get_text('illustrate'),msg)
            elif cid==9:
                if(len(psdmsg)==0):
                    reply = create_reply("should longer than 0",msg)
                else:
                    hwk = SetHomeworkHelper()
                    mhk = hwk.set(msg.create_time.strftime("%Y%m%d"),psdmsg)
                    reply = create_reply("sucess",msg)
            else:#uncoded message type
                if known_user==1:
                    user_d,user_d_rev = get_all_userlist()
                    name = user_d[codes['name_id']]
                    reply=create_reply(name+get_text('namago')+get_text('default')+get_text('gethelp'),msg)
                else:
                    reply = create_reply(get_text('uninituser')+get_text('gethelp'),msg)
            #reply = create_reply(msg.content, msg)
        elif msg.type == 'event':
            if msg.event == 'subscribe':
                reply = create_reply(get_text('subscribe')+get_text('gethelp'),msg)
            else:    
                reply = create_reply('Sorry, can not handle this for now', msg)
        else:    
            reply = create_reply('Sorry, can not handle this for now', msg)
        return crypto.encrypt_message(
            reply.render(),
            nonce,
            timestamp
        )


if __name__ == '__main__':
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.run('127.0.0.1', 5000, debug=True)
