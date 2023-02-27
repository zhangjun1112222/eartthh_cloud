import pytest
import yaml

from config.config import ServerInfo

import requests

from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '租户管理', skip_first=True)

with open(f'{data_path}/test_tenant.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
    # print(data)

class TestTenant:
    """
    租户管理
    """

    @pytest.mark.parametrize("name,probation,probation_begin,probation_end,system_name", data['新增租户数据'])
    def test_tenant_add(self, test_login, name, probation, probation_begin, probation_end, system_name):
        """
        新增租户
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        d = eval(DATA[0][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.json()['code'] == DATA[0][4]
        assert res.status_code == DATA[0][4]

    def test_tenant_querylist(self, test_login):
        """
        分页查询
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        d = eval(DATA[1][3])
        res = requests.get(url=u, headers=h, params=d)
        assert res.json()['code'] == DATA[1][4]
        assert res.status_code == DATA[1][5]

    def test_tenant_list(self, test_login):
        """
        获取列表所有数据
        """
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        res = requests.get(url=u, headers=h)
        # print(res.json())
        assert res.json()['code'] == DATA[2][4]
        assert res.status_code == DATA[2][5]
        return res.json()['data']['list'][-1]['id']

    def test_tenant_update(self, test_login):
        """
        修改租户信息
        """
        a = self.test_tenant_list(test_login)
        u = ServerInfo.get_url(eval(DATA[3][1]))
        h = eval(DATA[3][2])
        b = '租户333'
        d = eval(DATA[3][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.json()['data']['name'] == eval(DATA[3][5])
        assert res.status_code == DATA[3][4]

    def test_tenant_delete(self, test_login):
        """
        删除租户
        """
        a = self.test_tenant_list(test_login)
        u = ServerInfo.get_url(eval(DATA[4][1]))
        h = eval(DATA[4][2])
        res = requests.delete(url=u, headers=h)
        assert res.json()['data'] == eval(DATA[4][5])
        assert res.status_code == DATA[4][4]



