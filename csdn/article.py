
import threading
from queue import Queue
import requests
import json
import time
import pdfkit




class LaGou_Article_Spider():
    def __init__(self,url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            # 'Cookie': 'cookie信息',
            'Cookie': 'user_trace_token=20200903005614-12d25d1e-9e9f-4da0-8cfc-775470cf8b62; _ga=GA1.2.1328625610.1599065775; LGUID=20200903005614-50933e54-23d5-4b9e-9e8c-1c6a888d4c77; LG_HAS_LOGIN=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1599065775,1600698164; LG_LOGIN_USER_ID=6c501b589db168d007324ef899277ce470cc61f12fa1833edfed9da7e7aee83d; user-finger=2322fc0ab563ac59465fc725452ec92e; sensorsdata2015session=%7B%7D; _putrc=64417A06EC1584D4123F89F2B170EADC; login=true; unick=%E8%B5%B5%E7%85%9C%E4%B8%9C; gate_login_token=72e9c60fdba9ef49e9ff472ba83bf78e929592d2ed3b7fe4261e34b16256b888; X_HTTP_TOKEN=8db7f774800c84454969152061184d183a58dd69e1; JSESSIONID=2BD725E5ED9CA9BE8A02EAE4ACB21CB1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2210794337%22%2C%22%24device_id%22%3A%221744fbf5ad286c-0f51254c3f24b3-f7b1332-2073600-1744fbf5ad3cc9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22App%22%2C%22%24latest_utm_medium%22%3A%22%E8%AE%AD%E7%BB%83%E8%90%A5%E4%B8%93%E5%8C%BA%22%2C%22%24latest_utm_term%22%3A%22java3214%22%2C%22%24latest_utm_campaign%22%3A%22App%E8%AE%AD%E7%BB%83%E8%90%A5%E4%B8%93%E5%8C%BA%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2285.0.4183.121%22%7D%2C%22first_id%22%3A%221751d9ad701219-0ae4130382a182-333376b-2073600-1751d9ad702dfb%22%7D',
            # 'Referer': 'https://kaiwu.lagou.com/course/courseInfo.htm?courseId=17',
            'Referer': 'https://kaiwu.lagou.com/course/courseInfo.htm?courseId=492',
            'Origin': 'https://kaiwu.lagou.com',
            'Sec-fetch-dest': 'empty',
            'Sec-fetch-mode': 'cors',
            'Sec-fetch-site': 'same-site',
            'x-l-req-header': '{deviceType:1}'}
        self.textUrl='https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessonDetail?lessonId='  #发现课程文章html的请求url前面都是一样的最后的id不同而已
        self.queue = Queue()  # 初始化一个队列
        self.error_queue = Queue()

    def parse_one(self):
        """

        :return:获取文章html的url
        """
        # id_list=[]
        html = requests.get(url=self.url, headers=self.headers).text
        dit_message = json.loads(html)
        message_list = dit_message['content']['courseSectionList']
        # print(message_list)
        for message in message_list:
            for i in message['courseLessons']:
                true_url=self.textUrl+str(i['id'])
                self.queue.put(true_url)#文章的请求url


        return self.queue

    def get_html(self,true_url):
        """

        :return:返回一个Str 类型的html
        """
        global article_name
        html=requests.get(url=true_url,timeout=10,headers=self.headers).text
        dit_message = json.loads(html)
        str_html=str(dit_message['content']['textContent'])
        article_name1=dit_message['content']['theme']
        if "|" or '?' or '/' in article_name1:
            article_name=article_name1.replace("|"and'?'and'/', "-")
        else:
            article_name=article_name1
        self.htmltopdf(str_html,article_name)

    def htmltopdf(self,str_html,article_name):
        path_wk = r'D:\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wk)
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
            'custom-header': [('Accept-Encoding', 'gzip')]
        }
        pdfkit.from_string(str_html,"D:\\video\\{}.pdf".format(article_name),configuration=config,options=options)



    def thread_method(self, method, value):  # 创建线程方法
        thread = threading.Thread(target=method, args=value)
        return thread

    def main(self):

        thread_list = []
        true_url= self.parse_one()
        while not  true_url.empty():
            for i in range(10):  # 创建线程并启动
                if not true_url.empty():
                    m3u8 = true_url.get()
                    print(m3u8)
                    thread = self.thread_method(self.get_html, (m3u8,))
                    thread.start()
                    print(thread.getName() + '启动成功,{}'.format(m3u8))
                    thread_list.append(thread)
                else:
                    break
            while len(thread_list)!=0:
                for k in thread_list:
                    k.join()  # 回收线程
                    print('{}线程回收完毕'.format(k))
                    thread_list.remove(k)


if __name__ =="__main__":
    url='https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId=492'
    run = LaGou_Article_Spider(url)
    run.main()


