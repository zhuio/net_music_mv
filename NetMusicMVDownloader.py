import requests
import os
import re
class NetMV:
    def __init__(self, url):
        self.url = url
        self.mv_id = []
        self.mv_urls = []
    def generate(self):
        id = re.findall(r'id=(.*)',self.url)[0]
        j = requests.get('https://api.imjad.cn/cloudmusic/?type=playlist&id=%s' % id).json()
        ll = len(j['privileges'])
        # 获取MV ID
        for i in range(0,ll):
            if j['playlist']["tracks"][i]['mv'] != 0:
                self.mv_id.append(j['playlist']["tracks"][i]['mv'])
        # 获取MV的URL
        for id in self.mv_id:
            self.mv_urls.append('https://api.imjad.cn/cloudmusic/?type=mv&id=%s' % id)

    def download(self):
        pwd = os.path.abspath('.')
        directory = pwd +'/'+'MV'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for mv_url in self.mv_urls:
            name = requests.get(mv_url).json()['data']['name']
            if os.path.exists(directory+'/'+'%s.mkv' % name) == True:
                print('已经下载过这首歌曲了，跳过......')
            else:
                url = requests.get(mv_url).json()['data']['brs']['1080']
                r = requests.get(url)
                print('开始下载%s到当前的文件夹' % name)
                with open(directory+'/'+'%s.mkv' % name, 'wb') as f:
                    f.write(r.content)
        print('下载结束，看看去吧')

def main():
    print('输入歌单所在的网址')
    nv = NetMV(url = input())
    nv.generate()
    nv.download()
if __name__ == '__main__':
    main()
