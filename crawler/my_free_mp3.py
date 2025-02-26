# -*- coding: utf-8 -*-
import io
import os
import sys
import requests
import json
import time
import subprocess
from functools import partial
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
import execjs
from urllib.parse import urlencode, urljoin
timestamp_seconds = time.time()
timestamp_milliseconds = int(timestamp_seconds * 1000)
os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
# 修改 subprocess 的编码处理
subprocess.Popen = partial(subprocess.Popen,
                         encoding='utf-8',
                         errors='ignore',
                         env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "逆向js文件", "free_mp3_code.js")
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://tool.liumingye.cn",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}
cookies = {
    "__gads": "ID=eff7ab1e3865e369:T=1738933134:RT=1738933134:S=ALNI_MYj9gf_gbrPxv9ukx3vOAMQDun0gw",
    "__gpi": "UID=0000102ce16be293:T=1738933134:RT=1738933134:S=ALNI_MZLAe1tZ8HfQqYM6XIgLFbFyaS-KA",
    "__eoi": "ID=a42882c3297eb158:T=1738933134:RT=1738933134:S=AA-AfjaX_OR6XB4a52CypvNc67WJ",
    "cf_clearance": "rCfQ_d77_R67eRkJi6Rn6D8DW8HjRfGyVYD8UhFkI9c-1738936581-1.2.1.1-X5cbXtWaue1KQvAgh09tkrrY_kBzvAeSAiew7JfKFoCQgQimYP0_RqdlBKzxNRmowKqCpMCn0TPJ1Of0wWhBVKRMXQIE5CYgcxzngLCdgpDWPI60d8FOLHEpzoavupfX77LLG5pZxBBOSRMHjr8c8Q1a4YAxz81MF0Rgr_vv.a7.sAPm0tN0NDzyK79TlJC5jhU8oN5fMIyKgKeCO7VQNNrtDl9OwNracdEz76TI.7JS85ktN.AZTJ9oWr078IDJdJrukfZyGn7PA53AeyoxK4X5GrPNZeNTxc6P.yv_C4g"
}
def check_data_encoding(data):
    """
    检查数据编码并进行必要的转换
    """
    if isinstance(data, dict):
        return {k: check_data_encoding(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [check_data_encoding(item) for item in data]
    elif isinstance(data, str):
        try:
            # 尝试编码解码来确保数据可以正确处理
            return data.encode('utf-8').decode('utf-8')
        except UnicodeError:
            # 如果有问题的字符，可以选择替换或删除
            return data.encode('utf-8', errors='ignore').decode('utf-8')
    return data
def get_rsearch(name):
    search_url = "https://tool.liumingye.cn/music/api/search"
    encrypt_data = f'{{"type":"YQM","text":"{name}","page":1,"v":"beta","_t":{timestamp_milliseconds}}}'
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        js_context = execjs.compile(f.read()).call('token',encrypt_data)
        search_data = {
            "type": "YQM",
            "text": f"{name}",
            "page": 1,
            "v": "beta",
            "_t": timestamp_milliseconds,
            "token": f"{js_context}"
        }
        search_data = json.dumps(search_data, separators=(',', ':'))
        response = requests.post(url=search_url, headers=headers, cookies=cookies, data=search_data)
        response.encoding = 'utf-8'  # 强制使用UTF-8解码
        res = response.json()
        i=res['data']['list']
        res_finally={"songs":[{
            "SongName":song['name'],
            "SingerName":song['artist'][0]['name'],
            "img":song['album']['pic'] if 'album' in song else song['pic'],
            'play_url':get_play_url(song['id'] if len(song['id']) > 10 else song['hash']),
            "lyrics": ""
        }for song in i]}
        check_data_encoding(res_finally)
        return res_finally

def get_play_url(hash_id):
    play_url = "https://tool.liumingye.cn/music/api/link"
    encrypt_data = f'{{"id":"{hash_id}","quality":"128","_t":"{timestamp_milliseconds}"}}'
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        js_context = execjs.compile(f.read()).call('token',encrypt_data)
        play_data = {
            "id": f"{hash_id}",
            "quality": 128,
            "_t": f"{timestamp_milliseconds}",
            "token": f"{js_context}"
        }
        query_string = urlencode(play_data)

        full_url = urljoin(play_url, '?' + query_string)
        return full_url
if __name__ == '__main__':
    print(get_rsearch('nonsense'))