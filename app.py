from __future__ import absolute_import, unicode_literals
import os
from flask import Flask, request, abort, render_template
from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException

from message import message
from sqlite_helper import SQLiteHelper
from hwk_helper import HomeworkHelper
from time_helpter import timestamp2date
import sys
# set token or get from environments
TOKEN = os.getenv('WECHAT_TOKEN', 'imneo')
EncodingAESKey = os.getenv('WECHAT_ENCODING_AES_KEY', '1wGqo5kzdHNETfD56xqsN7WNP9TBBIMZDogPdKxTIYb')
AppId = os.getenv('WECHAT_APP_ID', 'wxb580d81e415849e1')

app = Flask(__name__)


@app.route('/')
def index():
    host = request.url_root
 #   return render_template('index.html', host=host)
    return "hello world"

from util import *

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
            print("openidis %s\n" %appuserid)
            content=SQLiteHelper()
            codes=content.get(appuserid)
            print(codes)
            known_user=0
            if 'name' in codes.keys():
                known_user=1
            if cid==1:
               #homework 
                if known_user==1:
                    name = codes['name']
                    nameid = codes['name_id']
                    hwk = HomeworkHelper(str(msg.create_time.year)+'Y'+str(msg.create_time.month)+'M'+str(msg.create_time.day)+'D')
                    hwk.set(nameid,psdmsg)
                else:
                    reply = create_reply(get_text('unintuser'),msg)
            elif cid==2:
                #updatename
                user_d,user_d_rev = get_userlist()
                name,errcode = check_existence(psdmsg,user_d)
                if errcode==1:
                    codes.update({'name':name})
                    codes.update({'name_id':user_d_rev[name]})
                    content.set(appuserid,codes)
                    reply = create_reply(name+get_text('namago')+get_text('thx'),msg)
                else:
                    reply = create_reply(name+get_text('unknownuser'),msg)
            else:#uncoded message type
                if known_user==1:
                    reply=create_reply(codes['name']+get_text('namago')+get_text('default'),msg)
                else:
                    reply = create_reply(get_text('uninituser'),msg)
            #reply = create_reply(msg.content, msg)
        elif msg.type == 'event':
            if msg.event == 'subscribe':
                reply = create_reply(get_text('subscribe'),msg)
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
    app.run('127.0.0.1', 5000, debug=True)
