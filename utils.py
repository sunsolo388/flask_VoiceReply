import os
import base64
import json
import requests
import pandas as pd
import jieba
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)

CUID = 'my_unique_client_id'


def get_access_token(api_key, secret_key):
    # 获取访问令牌
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'
    response = requests.get(url)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        logging.debug(f"Access token: {access_token}")
        return access_token
    else:
        logging.error(f"Failed to get access token: {response.text}")
        raise Exception("Failed to get access token")


def speech_to_text(audio_data, access_token):
    if not audio_data or len(audio_data) == 0:
        logging.error("No audio data provided or audio data is empty.")
        return "未提供有效的音频数据"

    url = 'http://vop.baidu.com/server_api'
    headers = {
        'Content-Type': 'application/json',
    }

    audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    logging.debug(f"Base64 audio length: {len(audio_base64)}")

    data = {
        'dev_pid': 1537,  # 识别普通话
        'format': 'wav',  # 这里保持为wav，确保和音频格式匹配
        'rate': 16000,    # 确保采样率正确
        'token': access_token,
        'cuid': CUID,     # 你的设备标识
        'channel': 1,     # 单声道
        'speech': audio_base64,
        'len': len(audio_data)  # 添加音频数据长度
    }

    logging.debug(f"Request data: {json.dumps(data)}")

    response = requests.post(url, headers=headers, data=json.dumps(data))

    logging.debug(f"Response Status Code: {response.status_code}")
    logging.debug(f"Response Content: {response.content}")

    if response.status_code == 200:
        result = response.json()
        logging.debug(f"Response JSON: {result}")
        if result['err_no'] == 0:
            return result['result'][0]
        else:
            logging.error(f"Error in speech_to_text: {result['err_no']}, {result['err_msg']}")
            return f"识别失败: {result['err_msg']}"
    else:
        logging.error(f"ASR API request failed: {response.text}")
        return "我不太明白你在说什么，请提供更多详细信息。"


def extract_keywords(text):
    words = jieba.lcut(text)
    return [word for word in words if len(word) > 1]


def load_keywords_from_excel(file_path):
    df = pd.read_excel(file_path)
    keyword_dict = dict(zip(df['关键词'], df['回复']))
    return keyword_dict


def generate_response(keywords, keyword_dict):
    best_match = None
    max_match_count = 0

    for keyword, response in keyword_dict.items():
        match_count = sum(1 for k in keywords if k in keyword)
        if match_count > max_match_count:
            max_match_count = match_count
            best_match = response

    return best_match or "我不太明白你在说什么，请提供更多详细信息。"


def text_to_speech(text, access_token, spd=5, pit=5, vol=5, per=4, emphasis=None):
    if emphasis:
        emphasized_text = f"<prosody pitch='+{emphasis}'>{text}</prosody>"
    else:
        emphasized_text = text

    url = 'https://tsn.baidu.com/text2audio'
    params = {
        'tex': emphasized_text,
        'tok': access_token,
        'cuid': CUID,
        'ctp': 1,
        'lan': 'zh',
        'spd': spd,
        'pit': pit,
        'vol': vol,
        'per': per,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.content
    logging.error(f"Text to speech request failed: {response.text}")
    return None


def save_audio_file(audio_data):
    if not os.path.exists('voice_resource'):
        os.makedirs('voice_resource')

    filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    filepath = os.path.join('voice_resource', filename)

    audio_data.save(filepath)
