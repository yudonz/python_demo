import requests


def get_data():
    url = "https://zhuanlan.zhihu.com/p/88710516"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    resp = requests.get(url, headers=headers)  # Get方式获取网页数据
    print(resp.status_code)  # 网页的返回值
    # print(resp.text)  # 网页的内容
    with open('知乎.html', 'w', encoding='utf-8') as f:
        f.write(resp.text)


if __name__ == '__main__':
    get_data()
