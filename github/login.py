'''

POST请求自动登录github。
    github反爬:
        1.session登录请求需要携带login页面返回的cookies
        2.email页面需要携带session页面后的cookies
'''

import re

import requests

# 一 访问login获取authenticity_token

login_url = 'https://github.com/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Referer': 'https://github.com/'
}
login_res = requests.get(login_url, headers=headers)
# print(login_res.text)
authenticity_token = re.findall('name="authenticity_token" value="(.*?)"', login_res.text, re.S)[0]
# print(authenticity_token)
login_cookies = login_res.cookies.get_dict()


def login():
    login_res = requests.get(login_url, headers=headers)
    print(login_res.status_code)
    print(login_res.content)
    authenticity_token = re.findall('name="authenticity_token" value="(.*?)"', login_res.text, re.S)[0]
    print(authenticity_token)
    # login_cookies = login_res.cookies.get_dict()
    # print(login_cookies)
    print("login结束")


if __name__ == '__main__':
    login()

# 二 携带token在请求体内往session发送POST请求
session_url = 'https://github.com/session'

session_headers = {
    'Referer': 'https://github.com/login',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}

form_data = {
    "commit": "Sign in",
    "utf8": "✓",
    "authenticity_token": authenticity_token,
    "login": "username",
    "password": "githubpassword",
    'webauthn-support': "supported"
}

# 三 开始测试是否登录
session_res = requests.post(
    session_url,
    data=form_data,
    cookies=login_cookies,
    headers=session_headers,
    # allow_redirects=False
)

session_cookies = session_res.cookies.get_dict()

url3 = 'https://github.com/settings/emails'
email_res = requests.get(url3, cookies=session_cookies)

print('账号' in email_res.text)

# 自动登录github（手动处理cookies信息）
