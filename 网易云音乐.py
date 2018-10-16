import requests
from bs4 import BeautifulSoup
import re
import threading
from multiprocessing import Process,Lock
from multiprocessing import Pool
import time
from tqdm import tqdm


filename='comment_post'#保存的文件名
keyword='民摇'#搜索关键词
titleList=[]#歌曲信息
userList=[]#评论者信息
commentList = []  # 评论

playLink=[]#歌单列表
songIdList=[]#歌曲id列表
song=0
headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3",
            'Connection': 'close'
}


def get_proxy():
    return requests.get("http://localhost:5010/get/",timeout=15).content

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

def makeProxy():
    print('获取代理ip中')
    try:
        with Lock():
            proxy = "http://"+str(get_proxy()).strip('b').strip('\'')
    except:
        proxy=""

    r = requests.get('http://music.163.com/api/v1/resource/comments/R_SO_4_%s?limit=100&offset=0' % songIdList[0],
                     timeout=10, headers=headers, proxies={"http":  proxy})
    try:
        r.json()
        print(proxy)
        return proxy
    except:
        print('fake id')
        delete_proxy(proxy)
        makeProxy()

def getHTMLText(url):
    try:
        r=requests.get(url,headers=headers)
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return 'error'

def fetchPlayList(keyword):
     for i in range(0,1):
        r = requests.get('https://music.163.com/discover/playlist?order=hot&cat='+keyword+'&limit=35&offset='+str(i*35), headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        playList = soup.find_all('a', class_='msk')
        for i in playList:
            playLink.append('https://music.163.com/' + i.get('href'))

def fetchSongList(url):#url为歌单链接
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    songList = soup.select('a[href*="song?id="]')
    for i in songList:
        id = re.findall(r'\d+', i.get('href'))
        if len(id) != 0:
            songIdList.append(id[0])



def getCommand(id,proxy):
    for page in range(0,101):
        try:
            print('Getting page%d'%page)
            r=requests.get('http://music.163.com/api/v1/resource/comments/R_SO_4_%s?limit=100&offset=%d'%(id,page*100), headers=headers,proxies={"http":  proxy},timeout=15)
            #r = requests.get('http://music.163.com/api/v1/resource/comments/R_SO_4_%s?limit=100&offset=%d' % (id, page * 100),headers=headers,timeout=30)
            result = r.json()
            code=result["code"]
            if code==-460:
                print('IP is dead ,change IP')
                with Lock():
                    proxy=makeProxy()
                continue
            comments = result['comments']
            for i in comments:
                commentList.append(i['content'])
               # userList.append(i['user']['nickname'] + ':' + str(i['user']['userId']))
            if result['more'] == False:
                break
        except Exception as e:
            with Lock():
                print(e)
                delete_proxy(proxy)
                makeProxy()
                continue

def getLyric(id,proxy):
    try:
        #r=requests.get('http://music.163.com/api/song/lyric?os=pc&id=%s&lv=-1&kv=-1&tv=-1'%id, headers=headers,proxies={"http": "http://" + proxy},timeout=15)
        r = requests.get('http://music.163.com/api/song/lyric?os=pc&id=%s&lv=-1&kv=-1&tv=-1' % id, headers=headers, timeout=15)
        result = r.json()
        code=result["code"]
        # if code==-460:
        #     print('IP is dead ,change IP')
        #     proxy=makeProxy()
            #return proxy
        lrc = result['lrc']['lyric']
        #print(lrc)
        lrcList.append(lrc)
    except:
        #proxy=makeProxy()
        print('error')
        #return proxy


def commandThread(name,start,end):
    global song,commentList,lrcList


    lrcList=[]#歌词列表
   # proxy = makeProxy()
    proxy=''
    for i in songIdList[start:end]:
        print('Process %s is running: Num.%d song' % (name,song))
        getCommand(i,proxy)
        #getLyric(i,proxy)
        song += 1


    for j in commentList:
        with open(filename+'.txt', 'a') as fd:
            fd.write(j)

    # for k in lrcList:
    #     with open(filename+'.txt', 'a') as fd:
    #         fd.write(k)
    # with lock:
    #     fd = open(filename+'.txt', "a")
    #     for k in lrcList:
    #         fd.write(k)
    #
    #     fd.close()
    print("%s is finished" %name)

def save():
    global commentList
    with Lock():
        for i in commentList:
            with open(filename+'.txt', 'a') as fd:
                fd.write(i)

def part():
    return int(len(songIdList)/4)

def Bar(arg):
    print(arg)
    save()

if __name__ == '__main__':
    threads=[]
    fetchPlayList(keyword)
    #lock=Lock()

    for i in tqdm(playLink[4:5]):    #获取歌单里每首歌的ID
        fetchSongList(i)

    songIdList = list(set(songIdList))
    print('There is %d songs totally' % len(songIdList))

    pool = Pool(processes=4)
    pool.apply_async(commandThread,('p1',0, part()),error_callback=Bar,callback=save)
    pool.apply_async(commandThread,('p2',part()+1,2*part()),error_callback=Bar,callback=save)
    pool.apply_async(commandThread,('p3',2*part()+1,3*part()),error_callback=Bar,callback=save)
    pool.apply_async(commandThread, ('p4',3*part()+1,None),error_callback=Bar,callback=save)


    pool.close()
    pool.join()

    print('Done')