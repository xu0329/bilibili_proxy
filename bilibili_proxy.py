import requests
import time
import requests
import threading
from fake_useragent import UserAgent


#使用前确保proxy.txt中有可用代理


#视频bv号放这里，格式如下

bvid=["xxxx","xxxx"]



lock=threading.Lock()


url = "http://api.bilibili.com/x/click-interface/click/web/h5"


headers = {
    'User-Agent':UserAgent().random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive'
}

reqdata = []
for bv in bvid:
    stime = str(int(time.time()))
    print("正在获取data，请耐心等待。。。")
    while True:
        resp = requests.get("http://api.bilibili.com/x/web-interface/view?bvid={}".format(bv))
        resp_json = resp.json()
        if "data" in resp_json:
            getdata = resp_json["data"]
            break
    data= {
        'aid':getdata["aid"],
        'cid':getdata["cid"],
        "bvid": bv,
        'part':'1',
        'mid':getdata["owner"]["mid"],
        'lv':'6',
        "stime" :stime,
        'jsonp':'jsonp',
        'type':'3',
        'sub_type':'0',
        'title': getdata["title"]
    }
    reqdata.append(data)





def process_lines(lines):
    # 在这里处理行
    for line in lines:
        ip=line.strip()
        proxies = {
            'http': 'http://' + ip,
        }

        try:
            for data in reqdata:
                stime = str(int(time.time()))
                data["stime"] = stime
                headers["referer"] = "http://www.bilibili.com/video/{}/".format(data.get("bvid"))
                requests.post(url,headers=headers,data=data,proxies=proxies,timeout=2)

            lock.acquire()
            with open('proxy.txt', 'a', encoding='utf-8') as f:
                f.write(ip+"\n")
                f.flush()
            lock.release()
            

        except Exception as e:
            print("代理连接超时")
        print("done   {}".format(ip))



def run():
    with open('proxy.txt', 'r', encoding='utf-8') as f:
        if f.read() == "":
            # 如果文件为空，就不执行
            print("proxy.txt中无代理")
            return
        

    with open('proxy.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # 清空文件
    with open('proxy.txt', 'w', encoding='utf-8') as f:
        f.write("")

    # 计算每个线程需要处理的行数
    if len(lines) < 50:
        threadnum=len(lines)
        lines_per_thread = len(lines)//len(lines)
    else:
        threadnum=50
        lines_per_thread = len(lines) // 50

    threads = []
    

    for i in range(threadnum):
        # 计算这个线程需要处理的行的起始和结束索引
        start = i * lines_per_thread
        end = start + lines_per_thread if i < (threadnum-1) else None  # 最后一个线程处理剩余的所有行

        # 创建一个新线程来处理这些行
        thread = threading.Thread(target=process_lines, args=(lines[start:end],))
        
        thread.start()
        threads.append(thread)


run()

