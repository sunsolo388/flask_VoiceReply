# coding=utf-8

import sys
import json
import base64
import time

IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError
    from urllib.parse import urlencode

    timer = time.perf_counter
else:
    from urllib2 import urlopen, Request, URLError
    from urllib import urlencode

    timer = time.clock if sys.platform == "win32" else time.time

API_KEY = 't53jRW0Yd5QPSYr7nvrqQxqY'  # 替换为你的API_KEY
SECRET_KEY = 'p62EuAzhpxnzIFE1xRiqWFjn3iyNyeCz'  # 替换为你的SECRET_KEY

# 需要识别的文件
AUDIO_FILE = 'D:\\PythonProject\\flaskProject\\static\\1.wav'  # 只支持 pcm/wav/amr 格式
FORMAT = AUDIO_FILE[-3:]  # 文件后缀

CUID = '123456PYTHON'
RATE = 16000  # 固定值

DEV_PID = 1537  # 识别普通话
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'


class DemoError(Exception):
    pass


TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'


def fetch_token():
    params = {
        'grant_type': 'client_credentials',
        'client_id': API_KEY,
        'client_secret': SECRET_KEY
    }
    post_data = urlencode(params)
    if IS_PY3:
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)

    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()

    if IS_PY3:
        result_str = result_str.decode()

    result = json.loads(result_str)
    if 'access_token' in result and 'scope' in result:
        if SCOPE and (SCOPE not in result['scope'].split(' ')):
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


if __name__ == '__main__':
    token = fetch_token()

    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
    speech = base64.b64encode(speech_data).decode('utf-8')

    params = {
        'dev_pid': DEV_PID,
        'format': FORMAT,
        'rate': RATE,
        'token': token,
        'cuid': CUID,
        'channel': 1,
        'speech': speech,
        'len': length
    }

    post_data = json.dumps(params, sort_keys=False).encode('utf-8')
    req = Request(ASR_URL, post_data)
    req.add_header('Content-Type', 'application/json')

    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        print("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    if IS_PY3:
        result_str = result_str.decode('utf-8')
    print(result_str)
    with open("result.txt", "w") as of:
        of.write(result_str)
