import requests


def get_data():
    resp = requests.get("https://www.baidu.com/")  # Get方式获取网页数据
    print(resp)  # 网页的返回值
    print(resp.content)  # 网页的内容
