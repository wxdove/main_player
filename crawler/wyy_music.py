import os
import requests
import execjs
import subprocess
from functools import partial
from concurrent.futures import ThreadPoolExecutor
subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
HEADERS = {
    "^accept": "*/*^",
    "^accept-language": "zh-CN,zh;q=0.9^",
    "^content-type": "application/x-www-form-urlencoded^",
    "^nm-gcore-status": "1^",
    "^origin": "https://music.163.com^",
    "^priority": "u=1, i^",
    "^referer": "https://music.163.com/^",
    "^sec-ch-ua": "^\\^Google",
    "^sec-ch-ua-mobile": "?0^",
    "^sec-ch-ua-platform": "^\\^Windows^^^",
    "^sec-fetch-dest": "empty^",
    "^sec-fetch-mode": "cors^",
    "^sec-fetch-site": "same-site^",
    "^user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36^"
}
COOKIES =  {
    "^_iuqxldmzr_": "32",
    "_ntes_nuid": "25b24837f954369e682a6b4a7fff0d94",
    "WEVNSM": "1.0.0",
    "WM_TID": "ASnkuhgsTWxBVEUVFFLHStmYznGs0uGA",
    "ntes_utid": "tid._.FSF90NqlcJVEUkERVBKGHsmcyiGvcXw^%^252F._.0",
    "__remember_me": "true",
    "ntes_kaola_ad": "1",
    "_ntes_nnid": "25b24837f954369e682a6b4a7fff0d94,1766579875707",
    "__snaker__id": "ffd5nUUxWY2TjgnA",
    "nts_mail_user": "18982949308^@163.com:-1:1",
    "NTES_P_UTID": "kFcsoanRqdcAzetbxAWNZqtAmVakNBN9^|1775029393",
    "__csrf": "7abe42e582ecf0cffb76c1eacf20d843",
    "Hm_lvt_1483fb4774c02a30ffa6f0e2945e9b70": "1781003338",
    "HMACCOUNT": "CEA1EF9AD2C7D46B",
    "JSESSIONID-WYYY": "U^%^2F2Hy^%^5C7ZkidPWupnfKkcwR^%^5CYcWDYQm4wmhTBwnOdkp8sUyZT8dySxDkh4wDFGKC^%^5CNRi4Y8Qb9V^%^5Ct^%^2FfbMFTDr0pJfxfmB9BmjIpc1HyiUlP7dXsdxO7ORysFoVk0u4IFlve^%^2Fl80MwvwOcGH2tGiJNi^%^2BgE5PY4Pb4kFYzi4cVbj5AFcqjZ^%^3A1781005141216",
    "NMTID": "00OrvAD1Hx3qFx53012rppFeKfd4isAAAGerBJXzA",
    "WNMCID": "iihnwy.1781003355191.01.0",
    "WM_NI": "6WTe3X5BgTx9oGWE3EOO8YuRSk2y66FRG4L6BA^%^2FBCXNPBP^%^2BU0w8VSXW^%^2FSRemtlpxU8KN0Z4QSfnFjai^%^2F87Py0QhKWNQUjd0^%^2B0rBjMc^%^2FhxuBbhidmu3s2jAgg0JkjmHmPejI^%^3D",
    "WM_NIKE": "9ca17ae2e6ffcda170e2e6ee8df362ab8cc0b6fc49ac968aa3d15a928a8e82c73e8eb2a9b6b3638f89baa6d22af0fea7c3b92af6899c86b254f79ea9b5fb33ad9999a6b24f8d91f8baf85a91b5fe9ab53e868e89d5cf3e829fe1a3c2548e908eb1aa5ff4a9f8b7d25495f19db3e867b8b4c099d834899200bbb75b91baa2a7e96babf1f8d8d373f48fa8acd646938ba685b321f4ae8e8bd069edb8b896c16aacb7ac8ef839b1eea6a2e66df496a58bf044af90ab8bcc37e2a3",
    "sDeviceId": "YD-CseXyC9f65tFFxQAABODDoyZm3G^%^2FcHyR",
    "gdxidpyhxdE": "NnzHAJDoa7SwTz4fx^%^2BzCHlZCJJcw^%^2FTnkEitRsyRzQmIClC8xaZTWpvy3^%^2Fy49mAbhfsIn57u^%^2BzrXUL4w^%^5CtZ^%^2FevofSU1COsLLa5jd6mlShb^%^2FJ7Z7IxjzKmKMcW1JV^%^2Bzg^%^5CnwzjNldiOeKb^%^5CiCrm8Ypp7u7^%^5CO9rzRkwUaZGUE58u^%^2FGfGe4OG^%^3A1781004286236",
    "NTES_YD_SESS": "1v8z9kwfwQdc2KUCpUX_MHAMMNuNIEFgKXhgf3Htppm_7LHE7Muc9bwUTuYkUf5ILwuNHqQZFKMCzJ3UMpNlQX.xRZleqmXeQrj1zJ0UnZ1p38_Bc28bqVbPFJA_4zp5X1uEsUZVp9s.SEfZ6JQO7rDOVmllkThYwmdHFHd4CCA6V4wVw.nxZwhRUitIyto4GE4vh125PRSZO5aPiF9lj3ZC08_XA2FKRZYYxYNpL2D6x",
    "S_INFO": "1781003568^|0^|0^&60^#^#^|15258816320",
    "P_INFO": "15258816320^|1781003568^|1^|music^|00^&99^|null^&null^&null^#CN^&null^#10^#0^|^&0^|null^|15258816320",
    "MUSIC_U": "002A4292A269E9A31A0E6C03D2EC69BA6B35FEE862313D8A63618E9AA8478C11F6ECD7A6E58BBAEF4227D33EA8B4A6DDFC860BC35238D141E634158BEE4951D784A446F4AE63D66ABED42A1AFC5BC5ACADE116F18365C1D44FBC78F7BA9BA1F5A5483D3BD601E256F67EA5D7C27A03571DD462F2ABF37B9361B1158FF35FB0DF8FED2851A5058280585A3C5E3B2827210B273BDDEBA88E3B6679F35714559D601B08829EF430D42A1203C4EE3D1CF13D4C70AE22B96DDE1A88AA98C199CD9F7EDAE118B4B669A0A9CCE75FCEF308AAE4408FBB5744B58AE78706F04546EFC9D04E7BAD23002BCBFDC31074D49D0C96B676E4921797BC00403FC7B3584859C7A7A90F7041AB464BE5B9A4E99765AF9EEAC937CF08A9EC56DB48EFF9CC9F13F0FE5EAB3A05759A88204E5036C1F574DE653F9C69459C51CD02E8776660D096C770EFD6354DD36FE24E069A1EA15A2F3A9D153E84DF581F26C4A93FF7E7B88F98B50A664AC8D99AE77A48FD10CCDB70DD26BC2E77CAEFEB92800BF97FAD42D5AFD0B2113EA20C65DDFAB422E274EA480DDF1A",
    "Hm_lpvt_1483fb4774c02a30ffa6f0e2945e9b70": "1781003619^"
}

SEARCH_URL = "https://music.163.com/weapi/cloudsearch/get/web"
SONG_URL = "https://music.163.com/weapi/song/enhance/player/url/v1"
LYRIC_URL = "https://music.163.com/weapi/song/lyric"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(BASE_DIR, "逆向js文件", "code.js")

try:
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        js_context = execjs.compile(f.read())
except FileNotFoundError:
    raise RuntimeError(f"JavaScript 文件 {JS_FILE} 未找到。")


def generate_params(data):
    ee = '010001'
    ff = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    gg = '0CoJUm6Qyw8W8jud'
    return js_context.call('get_wyy', data, ee, ff, gg)


def search_music(song_name):
    search_data = {
        "s": song_name,
        "type": "1",
        "offset": "0",
        "total": "true",
        "limit": "90",
        "csrf_token": COOKIES["__csrf"],
    }
    encrypted_data = generate_params(str(search_data))
    data = {"params": encrypted_data['encText'], "encSecKey": encrypted_data['encSecKey']}
    response = requests.post(SEARCH_URL, headers=HEADERS, cookies=COOKIES, data=data)
    response.raise_for_status()
    res = response.json()
    songs_data = res.get("result", {}).get("songs", [])

    with ThreadPoolExecutor(max_workers=5) as executor:
        lyrics = list(executor.map(get_lyric, [song['id'] for song in songs_data]))

    return {"songs":[{
        "SongName": song["name"],
        "SingerName": ", ".join(artist["name"] for artist in song["ar"]),
        "play_url": f"http://music.163.com/song/media/outer/url?id={song['id']}.mp3",
        "img": song["al"]["picUrl"],
        "lyrics": lyric
    } for song, lyric in zip(songs_data, lyrics)]}


def get_lyric(song_id):
    lyric_data = {"id": song_id, "lv": -1, "tv": -1, "csrf_token": COOKIES["__csrf"]}
    encrypted_data = generate_params(str(lyric_data))
    data = {"params": encrypted_data['encText'], "encSecKey": encrypted_data['encSecKey']}
    response = requests.post(LYRIC_URL, headers=HEADERS, cookies=COOKIES, data=data)
    response.raise_for_status()
    return response.json().get("lrc", {}).get("lyric", "歌词获取失败")



if __name__ == '__main__':
    song_name = input('输入歌名:')
    print(search_music(song_name))
