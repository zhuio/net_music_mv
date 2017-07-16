import requests
import os

print('请输入列表ID ')
PLAY_LIST_ID = input()
print('列表ID是 ',PLAY_LIST_ID)
print('正在解析API')

PLAY_LIST_JSON = requests.get('https://api.imjad.cn/cloudmusic/?type=playlist&id=%s' % PLAY_LIST_ID).json()

#获取MV ID
mv_id = []
def get_mv_id():
    for i in range(0,len(PLAY_LIST_JSON['privileges'])):
        if PLAY_LIST_JSON['playlist']["tracks"][i]['mv'] == 0:
            continue
        else:
            mv_id.append(PLAY_LIST_JSON['playlist']["tracks"][i]['mv'])
    return mv_id

#获取MV的URL
MV_API = 'https://api.imjad.cn/cloudmusic/?type=mv&id=5317050'
mv_urls = []
def get_mv_urls():
    for id in mv_id:
        mv_urls.append('https://api.imjad.cn/cloudmusic/?type=mv&id=%s' % id)
    return mv_urls

#下载歌曲
def download():

    pwd = os.path.abspath('.')
    directory = pwd +'/'+'MV'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for mv_url in mv_urls:
        name = requests.get(mv_url).json()['data']['name']
        if os.path.exists(directory+'/'+'%s.mkv' % name) == True:
            print('已经下载过这首歌曲了，跳过......')
            continue
        else:
            try:
                url = requests.get(mv_url).json()['data']['brs']['1080']
                r = requests.get(url)
                print('开始下载%s到当前的文件夹' % name)
                with open(directory+'/'+'%s.mkv' % name, 'wb') as f:
                    f.write(r.content)
            except Exception as e:
                print(e)
    print('下载结束，看看去吧')

if __name__ == '__main__':
    try:
        get_mv_id()
        get_mv_urls()
        download()
    except Exception as e:
        print('列表ID是否输对了啊？')
    finally:
        download()
