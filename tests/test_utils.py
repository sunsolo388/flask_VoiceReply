import unittest
import os
from config import API_KEY, SECRET_KEY,EXCEL_FILE_PATH  # 从config.py导入
from   utils import (
    get_access_token,
    speech_to_text,
    extract_keywords,
    load_keywords_from_excel,
    generate_response,
)

class TestUtils(unittest.TestCase):
    def setUp(self):
        # 替换为你的 API 密钥
        self.api_key = API_KEY#替换为自己的
        self.secret_key = SECRET_KEY#替换为自己的
        self.test_excel_path = EXCEL_FILE_PATH  # 你的 Excel 文件路径

        self.wav_file_path = './static/1.wav'  # 你的 WAV 文件路径

        # 获取访问令牌
        self.access_token = get_access_token(self.api_key, self.secret_key)

    def test_load_keywords_from_excel(self):
        # 测试从 Excel 加载关键词和回复
        try:
            keyword_dict = load_keywords_from_excel(self.test_excel_path)
            print(keyword_dict)  # 输出字典内容查看是否加载正确
            self.assertEqual(keyword_dict["天气"], "今天天气不错，适合出去走走。")
            self.assertEqual(keyword_dict["周末"], "这个周末有什么计划吗？")
            self.assertEqual(keyword_dict["晴天"], "哇，你运气真好！这个周末阳光明媚。")
        except Exception as e:
            self.fail(f"Failed to load keywords from Excel: {e}")

    def test_speech_to_text_with_wav(self):
        # 使用音频文件进行测试
        try:
            with open(self.wav_file_path, "rb") as audio_file:
                audio_data = audio_file.read()

            result = speech_to_text(audio_data, self.access_token)
            print(f"Speech to Text Result: {result}")  # 输出识别结果
            self.assertIsNotNone(result, "Failed to convert speech to text.")
        except Exception as e:
            self.fail(f"Error in speech_to_text: {e}")

        # 提取关键词
        keywords = extract_keywords(result)
        print(f"Extracted keywords: {keywords}")  # 调试信息
        self.assertTrue(keywords)

        # 生成回复
        keyword_dict = load_keywords_from_excel(self.test_excel_path)
        response = generate_response(keywords, keyword_dict)
        print(f"Generated response: {response}")  # 调试信息

        # 验证生成的回复
        self.assertIn(response, [
            "今天天气不错，适合出去走走。",
            "这个周末有什么计划吗？",
            "哇，你运气真好！这个周末阳光明媚。"
        ])

if __name__ == '__main__':
    unittest.main()
