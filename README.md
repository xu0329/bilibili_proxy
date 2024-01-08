#**问题**#
**目前每次请求都会更换useragent，如果不起作用可以修改对应部分代码**

**已知第二种方法用700个代理刷取播放量实际只能到150左右，不确定是什么问题**

**各位可以尝试单独用https，http代理，修改headers里的参数，请求的间隔时间等等方法来寻找刷播放量的最佳方式**

***有任何问题请提issue，也欢迎分享改进方法***
## [通过代理池刷播放量](bilibili_proxypool.py)
 

***所需安装依赖***
```python
pip install requests
```
 
**使用**：只需修改以下部分，运行即可  
![image](image/image.jpeg)


## [通过现有的代理刷播放量](bilibili_proxy.py)
使用前请确保[proxy.txt](proxy.txt)中有HTTP代理

每次运行都会去除不可用代理，添加代理可直接在末尾粘贴

***所需安装依赖***
```python
pip install fake_useragent
```
```python
pip install requests
```


**代理格式**

![image](image/proxy.jpeg)

## 免费代理
**[checkerproxy](https://checkerproxy.net/getAllProxy)**



## 代理池
[jhao104/proxy_pool](https://github.com/jhao104/proxy_pool)
