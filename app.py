# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify, request
import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import os
from crawler import wyy_music
from  crawler import kg_music
from crawler import  my_free_mp3
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  #
# 设置环境变量
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'en_US.UTF-8'

# 基础配置
app.config.update(
    JSON_AS_ASCII=False,
    JSONIFY_MIMETYPE='application/json; charset=utf-8'
)

@app.route('/')
def index():
    """主页面路由"""
    return render_template('index.html')

@app.route('/search1')
def search_api_wyy():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    try:
        result = wyy_music.search_music(query)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f'搜索失败: {str(e)}')
        return jsonify({'error': '搜索服务暂不可用'}), 500

@app.route('/search2')
def search_api_kg():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    try:
        result = kg_music.fetch_music(query)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f'搜索失败: {str(e)}')
        return jsonify({'error': '搜索服务暂不可用'}), 500


@app.route('/search3')
def search_api_free_mp3():
    query = request.args.get('q', '')
    query = query.encode('utf-8').decode('utf-8')
    if not query:
        return jsonify([])

    result = my_free_mp3.get_rsearch(query)
    return jsonify(result)


if __name__ == '__main__':
    app.static_folder = os.path.abspath('static')
    app.template_folder = os.path.abspath('templates')
    app.run(host='0.0.0.0', port=5000, debug=True)