import pytest
import re
from config.config import ServerInfo
from test.cases import data_path
import yaml
import requests
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '登陆登出', skip_first=True)


with open(f'{data_path}/test_tenant.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)


class TestLoginLogout:
    """
    系统登陆登出
    """

    @pytest.mark.parametrize("username,password,assert1,assert2", data['用户登陆数据'])
    def test_login(self, username, password, assert1, assert2):
        """
        登陆
        """
        u = ServerInfo.get_url(DATA[0][1])
        d = eval(DATA[0][3])
        res = requests.post(url=u, json=d)
        assert res.status_code == eval(DATA[0][4])
        assert res.json()['code'] == eval(DATA[0][5])

    def test_logout(self, test_login):
        """
        登出
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        res = requests.post(url=u, headers=h)
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
