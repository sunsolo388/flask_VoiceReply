# app.py

from flask import Flask, request, jsonify, session,send_from_directory,render_template
from flask_session import Session
import base64
import config
import utils
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # 使用文件系统存储会话
Session(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        audio_data = request.files['audio'].read()
        utils.save_audio_file(audio_data)  # 保存音频文件

        access_token = utils.get_access_token(config.API_KEY, config.SECRET_KEY)
        text = utils.speech_to_text(audio_data, access_token)

        logger.info(f"Recognized Text: {text}")

        if text:
            keywords = utils.extract_keywords(text)
            keyword_dict = utils.load_keywords_from_excel(config.EXCEL_FILE_PATH)
            response_text = utils.generate_response(keywords, keyword_dict)

            spd = int(request.args.get('spd', 5))
            pit = int(request.args.get('pit', 5))
            vol = int(request.args.get('vol', 5))
            per = int(request.args.get('per', 4))
            emphasis = request.args.get('emphasis')

            session['last_response'] = response_text
            session['last_spd'] = spd
            session['last_pit'] = pit
            session['last_vol'] = vol
            session['last_per'] = per
            session['last_emphasis'] = emphasis

            audio_response = utils.text_to_speech(response_text, access_token, spd, pit, vol, per, emphasis)
            if audio_response:
                return jsonify({
                    "response": response_text,
                    "audio": base64.b64encode(audio_response).decode('utf-8')
                })
        return jsonify({"error": "无法识别语音或生成响应"})
    except Exception as e:
        logger.error(f"Error in /transcribe: {e}")
        return jsonify({"error": "内部服务器错误"})

if __name__ == '__main__':
    app.run(debug=True)