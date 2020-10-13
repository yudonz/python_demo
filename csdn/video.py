import threading
from queue import Queue
import re
import requests
import json
from Crypto.Cipher import AES
import time
import os
import pdfkit


class LaGou_spider():
    def __init__(self,url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Cookie': 'user_trace_token=20200903005614-12d25d1e-9e9f-4da0-8cfc-775470cf8b62; _ga=GA1.2.1328625610.1599065775; LGUID=20200903005614-50933e54-23d5-4b9e-9e8c-1c6a888d4c77; LG_HAS_LOGIN=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1599065775,1600698164; LG_LOGIN_USER_ID=6c501b589db168d007324ef899277ce470cc61f12fa1833edfed9da7e7aee83d; user-finger=2322fc0ab563ac59465fc725452ec92e; sensorsdata2015session=%7B%7D; _putrc=64417A06EC1584D4123F89F2B170EADC; login=true; unick=%E8%B5%B5%E7%85%9C%E4%B8%9C; gate_login_token=72e9c60fdba9ef49e9ff472ba83bf78e929592d2ed3b7fe4261e34b16256b888; X_HTTP_TOKEN=8db7f774800c84454969152061184d183a58dd69e1; JSESSIONID=2BD725E5ED9CA9BE8A02EAE4ACB21CB1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2210794337%22%2C%22%24device_id%22%3A%221744fbf5ad286c-0f51254c3f24b3-f7b1332-2073600-1744fbf5ad3cc9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22App%22%2C%22%24latest_utm_medium%22%3A%22%E8%AE%AD%E7%BB%83%E8%90%A5%E4%B8%93%E5%8C%BA%22%2C%22%24latest_utm_term%22%3A%22java3214%22%2C%22%24latest_utm_campaign%22%3A%22App%E8%AE%AD%E7%BB%83%E8%90%A5%E4%B8%93%E5%8C%BA%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2285.0.4183.121%22%7D%2C%22first_id%22%3A%221751d9ad701219-0ae4130382a182-333376b-2073600-1751d9ad702dfb%22%7D',
            # 'Referer': 'https://kaiwu.lagou.com/course/courseInfo.htm?courseId=17',
            'Referer': 'https://kaiwu.lagou.com/course/courseInfo.htm?courseId=492',
            'Origin': 'https://kaiwu.lagou.com',
            'Sec-fetch-dest': 'empty',
            'Sec-fetch-mode': 'cors',
            'Sec-fetch-site': 'same-site',
            'x-l-req-header': '{deviceType:1}'}
        self.url='https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId=492'
        self.queue = Queue()  # 初始化一个队列
        self.error_queue = Queue()
    def get_id(self):
        ture_url_list=[]
        html = requests.get(url=self.url, headers=self.headers).text
        dit_message = json.loads(html)
        message_list = dit_message['content']['courseSectionList']
        for message in message_list:
            id1=message["courseLessons"]
            for t_id in id1:
                ture_url="https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail?lessonId={}".format(t_id["id"])
                ture_url_list.append(ture_url)
        return ture_url_list
    def parse_one(self,ture_url_list):
        """

        :return:获得所有的课程url和课程名 返回一个队列（请求一次）
        """
        for ture_url in ture_url_list:
            # print(ture_url)
            html = requests.get(url=ture_url, headers=self.headers).text
            # print(html)
            dit_message = json.loads(html)
            message_list = dit_message['content']
            # print(message_list["videoMedia"])
            if message_list["videoMedia"] == None:
                continue
            else:
                name=message_list["theme"]
                m3u8=message_list["videoMedia"]["fileUrl"]
                # print(m3u8)
                m3u8_dict = {m3u8:name}  # key为视频的url，val为视频的name
                if os.path.exists("{}.mp4".format(name)):
                    print("{}已经存在".format(name))
                    pass
                else:
                    # print(m3u8_dict)
                    self.queue.put(m3u8_dict)  # 将每个本地不存在的视频url（m3u8）和name加入到队列中
        # for message in message_list:
        #     # print(message)
        #     for i in message['courseLessons']:
        #         if i['videoMediaDTO'] == None:
        #             pass
        #         else:
        #             key = i['videoMediaDTO']['fileUrl']
        #             val = i['theme']
        #             m3u8_dict = {key: val}  # key为视频的url，val为视频的name
        #             # print(m3u8_dict)
        #
        return self.queue
    #
    def get_key(self, **kwargs):
        # global key
        m3u8_dict = kwargs
        # print(m3u8_dict)
        for k in m3u8_dict:  # 获取某个视频的url
            name = ''
            # print(k)
            true_url = k.split('/')[0:-1]
            t_url = '/'.join(true_url)  # 拼接ts的url前面部分
            html = requests.get(url=k, headers=self.headers).text  # 请求返回包含ts以及key数据
            # print(html)
            message = html.split('\n')  # 获取key以及ts的url
            key_parse = re.compile('URI="(.*?)"')
            key_list = key_parse.findall(html)
            # print("密匙链接"+key_list)
            # print(key_list[0])
            key = requests.get(url=key_list[0],
                               headers=self.headers).content  # 一个m3u8文件中的所有ts对应的key是同一个 发一次请求获得m3u8文件的key
            # print(key)
            name1 = m3u8_dict[k]  # 视频的名字
            # print("视频名："+name1)
            if "|" or '?' or '/' in name1:
                name = name1.replace("|" , "-")
                for i in message:
                    if '.ts' in i:
                        ts_url = t_url + '/' + i
                        # print("ts_url"+ts_url)
                        self.write(key, ts_url, name, m3u8_dict)
            else:
                name = name1
                for i in message:
                    # print(i)
                    if '.ts' in i:
                        ts_url = t_url + '/' + i
                        # print(ts_url)
                        self.write(key, ts_url, name, m3u8_dict)

    def write(self, key, ts_url, name01, m3u8_dict):
        dir='D:\\video'
        if not os.path.exists(dir):
            os.makedirs(dir)
        cryptor = AES.new(key, AES.MODE_CBC, iv=key)
        with open('{}\\{}.mp4'.format(dir,name01), 'ab')as f:
            try:
                html = requests.get(url=ts_url, headers=self.headers).content
                f.write(cryptor.decrypt(html))
                print('{}，{}写入成功'.format(ts_url, name01))
            except Exception as e:
                print('{}爬取出错'.format(name01))
                while True:
                    if f.close():  # 检查这个出问题的文件是否关闭  闭关则删除然后重新爬取，没关闭则等待10s，直到该文件被删除并重新爬取为止
                        os.remove('{}.mp4'.format(name01))
                        print('{}删除成功'.format(name01))
                        thread = self.thread_method(self.get_key, m3u8_dict)
                        print("开启线程{}，{}重新爬取".format(thread.getName(), name01))
                        thread.start()
                        thread.join()
                        break
                    else:
                        time.sleep(10)

    def thread_method(self, method, value):  # 创建线程方法
        thread = threading.Thread(target=method, kwargs=value)
        return thread

    def main(self):
        global m3u8
        thread_list = []
        ture_url_list=self.get_id()
        m3u8_dict = self.parse_one(ture_url_list)
        while not m3u8_dict.empty():
            for i in range(5):  # 创建线程并启动
                if not m3u8_dict.empty():
                    m3u8 = m3u8_dict.get()
                    # print(type(m3u8))
                    thread = self.thread_method(self.get_key, m3u8)
                    thread.start()
                    print(thread.getName() + '启动成功,{}'.format(m3u8))
                    time.sleep(1)
                    thread_list.append(thread)
                else:
                    break
            for k in thread_list:
                k.join()  # 回收线程


if __name__ == "__main__":


    run = LaGou_spider('')
    # run.get_id()
    time1 = time.time()
    run.main()
    time2 = time.time()
    print(time2 - time1)


