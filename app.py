from __future__ import absolute_import, unicode_literals
import os
from flask import Flask, request, abort, render_template
from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException

from message import message
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
            info = message()
            rpl,errid = info.msg_mng(msg.content,"data/hwd/"+str(msg.create_time.year)+'-'+str(msg.create_time.month)+'-'+str(msg.create_time.day))
            if(errid!=1):
                reply = create_reply(get_text(rpl),msg)
            else:
                reply = create_reply(rpl, msg)
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
