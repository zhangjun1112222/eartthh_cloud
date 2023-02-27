import pytest
import requests

from config.config import ServerInfo

@pytest.fixture(scope='function')
def test_login():
    u = ServerInfo.get_url('/tenant/user/login')
    d = {'username': 'admin', 'password': 'e10adc3949ba59abbe56e057f20f883e', "rememberMe": "false"}
    # 账号：admin 密码：123456

    res=requests.post(url=u, json=d)
    # print(res.json())
    return res.json()['data']['token']

@pytest.fixture(scope='function')
def test_login2():
    u = ServerInfo.get_url('/tenant/user/login')
    d = {'username': 'zj001', 'password': 'e10adc3949ba59abbe56e057f20f883e', "rememberMe": "false"}
    # 账号：admin 密码：123456

    res = requests.post(url=u, json=d)
    # print(res.json())
    return res.json()['data']['token']
