import hashlib
import time
import requests
import json
from fake_useragent import UserAgent
ua = UserAgent()
session=requests.Session()
def generate_signature(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()

def fetch_play_url(mix_song_id):
    local_time = int(time.time() * 1000)
    text = [
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
        "appid=1014",
        f"clienttime={local_time}",
        "clientver=20000",
        "dfid=11RQfS2Fwjxa2PXGrP2AtMBY",
        f"encode_album_audio_id={mix_song_id}",
        "mid=61af5064402d2bc3d834a9c2a65dbecf",
        "platid=4",
        "srcappid=2919",
        "token=",
        "userid=0",
        "uuid=61af5064402d2bc3d834a9c2a65dbecf",
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    ]
    data = "".join(text)
    signature = generate_signature(data)

    params = {
        "srcappid": "2919",
        "clientver": "20000",
        "clienttime": f"{local_time}",
        "mid": "61af5064402d2bc3d834a9c2a65dbecf",
        "uuid": "61af5064402d2bc3d834a9c2a65dbecf",
        "dfid": "11RQfS2Fwjxa2PXGrP2AtMBY",
        "appid": "1014",
        "platid": "4",
        "encode_album_audio_id": f"{mix_song_id}",
        "token": "",
        "userid": "0",
        "signature": f"{signature}"
    }
    url = "https://wwwapi.kugou.com/play/songinfo"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "origin": "https://www.kugou.com",
        "priority": "u=1, i",
        "referer": "https://www.kugou.com/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": f"{ua.random}"
    }
    try:
        response = session.get(url, headers=headers,params=params)
        result = response.json()
        return [result['data'].get('play_url', ''), result['data'].get('img', ''),result['data'].get('lyrics','')]
    except Exception as e:
        print(f"Error fetching play URL: {e}")
        return ""

def fetch_music(keyword):
    local_time = int(time.time() * 1000)
    text = [
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt",
        "appid=1014",
        "bitrate=0",
        "callback=callback123",
        f"clienttime={local_time}",
        "clientver=1000",
        "dfid=3x6k4z42n6FG4CnvV90WqHgx",
        "filter=10",
        "inputtype=0",
        "iscorrection=1",
        "isfuzzy=0",
        f"keyword={keyword}",
        "mid=60fed3a62a77c763aeb0f706db5c982e",
        "page=1",
        "pagesize=30",
        "platform=WebFilter",
        "privilege_filter=0",
        "srcappid=2919",
        "token=18bd6a34ed7deabdcb2a2a95d6cb97949fd7262d129a774fd27344d891b0a8aa",
        "userid=1069521587",
        "uuid=60fed3a62a77c763aeb0f706db5c982e",
        "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
    ]
    data = "".join(text)
    signature = generate_signature(data)
    params = {
        "callback": "callback123",
        "srcappid": "2919",
        "clientver": "1000",
        "clienttime": local_time,
        "mid": "60fed3a62a77c763aeb0f706db5c982e",
        "uuid": "60fed3a62a77c763aeb0f706db5c982e",
        "dfid": "3x6k4z42n6FG4CnvV90WqHgx",
        "keyword": keyword,
        "page": "1",
        "pagesize": "30",
        "bitrate": "0",
        "isfuzzy": "0",
        "inputtype": "0",
        "platform": "WebFilter",
        "userid": "1069521587",
        "iscorrection": "1",
        "privilege_filter": "0",
        "filter": "10",
        "token": "18bd6a34ed7deabdcb2a2a95d6cb97949fd7262d129a774fd27344d891b0a8aa",
        "appid": "1014",
        "signature": signature
    }
    cookies = {
        "kg_mid": "61af5064402d2bc3d834a9c2a65dbecf",
        "kg_dfid": "11RQfS2Fwjxa2PXGrP2AtMBY",
        "kg_dfid_collect": "d41d8cd98f00b204e9800998ecf8427e",
        "Hm_lvt_aedee6983d4cfc62f509129360d6bb3d": "1738834878,1738834962,1738834979,1738837683",
        "HMACCOUNT": "B2BFE85C6C1D3879",
        "kg_mid_temp": "61af5064402d2bc3d834a9c2a65dbecf",
        "Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d": "1738837695"
    }
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://www.kugou.com/",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-site",
        "user-agent": f"{ua.random}"
    }
    url = "https://complexsearch.kugou.com/v2/search/song"
    try:
        result = session.get(url, headers=headers,cookies=cookies,params=params).text[12:-2]
        result = json.loads(result)
        music_list = result.get('data', {}).get('lists', [])
        return {"songs":[{
            "SongName": music['SongName'],
            "SingerName": music['SingerName'],
            "play_url": fetch_play_url(music['EMixSongID'])[0],
            "img": fetch_play_url(music['EMixSongID'])[1],
            "lyrics": fetch_play_url(music['EMixSongID'])[2]
        } for music in music_list]}
    except Exception as e:
        print(f"Error fetching music: {e}")
        return []

if __name__ == '__main__':
    print(fetch_music('薛之谦'))