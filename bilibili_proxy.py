import requests
import time


#视频bv号放这里，格式如下

bvid=["xxxx","xxxx"]


#代理池地址，项目可见https://github.com/jhao104/proxy_pool

getproxy = "http://127.0.0.1:5010/get/"
deleteproxy = "http://127.0.0.1:5010/delete/?proxy={}"
proxynum="http://127.0.0.1:5010/count"



url = "http://api.bilibili.com/x/click-interface/click/web/h5"


headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.bilibili.com',
    'Connection': 'keep-alive'
}

reqdata = []
for bv in bvid:
    stime = str(int(time.time()))
    
    resp = requests.get("https://api.bilibili.com/x/web-interface/view?bvid={}".format(bv))
    getdata = resp.json()["data"]
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



def run():
    num=0
    while int(requests.get(proxynum).json().get("count")) != 0:

        resp=requests.get(getproxy).json().get("proxy")
        for data in reqdata:
            
            try:
                stime = str(int(time.time()))
                data["stime"] = stime
                headers["referer"] = "http://www.bilibili.com/video/{}/".format(data.get("bvid"))

                proxy = {
                    "http": "http://{}".format(resp)
                }

                requests.post(url,headers=headers,data=data,proxies=proxy,timeout=5)

            except Exception as e:
                print("代理连接超时")

        requests.get(deleteproxy.format(resp))
        num+=1
        print("done   {}".format(num))

    print("无可用代理")

run()
        
