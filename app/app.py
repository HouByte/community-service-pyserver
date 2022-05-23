# -*- coding: utf-8 -*-
# @Time : 2022/4/30 9:02
# @Author : Vincent Vic
# @File : app.py
# @Software: PyCharm
from application import app

# web server
if __name__ == '__main__':
    try:
        app.run(host="0.0.0.0", port=5000, load_dotenv=True)
    except Exception as e:
        import traceback
        traceback.print_exc()
