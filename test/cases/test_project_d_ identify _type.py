import pytest
import yaml
import random
from config.config import ServerInfo
import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '识别结果类型', skip_first=True)


class TestIdentifyType:
    """
    识别结果类型
    """

    def test_project_tenant_list(self, test_login):
        """
        租户列表
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[0][4]
        assert res.json()['code'] == DATA[0][5]
        # print(res.json()['data'][1]['name'])
        return res.json()['data'][-1]['id']

    def test_identify_type_query(self, test_login):
        """
        结果类型分页查询
        """
        a = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        d = eval(DATA[1][3])
        res = requests.get(url=u, headers=h, params=d)
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]

    def test_identify_type_add(self, test_login):
        """
        识别结果类型新增
        """
        c = random.randint(1000, 9999)
        a = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        d = eval(DATA[2][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]

    def test_identify_type_list(self, test_login):
        """
        识别结果类型列表
        """
        a = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]
        return res.json()['data']['list'][-1]['id']

    def test_identify_type_update(self, test_login):
        """
        识别结果类型修改
        """
        c = random.randint(1000, 9999)
        a = self.test_identify_type_list(test_login)
        b = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(eval(DATA[4][1]))
        h = eval(DATA[4][2])
        d = eval(DATA[4][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]

    def test_identify_type_add2(self, test_login):
        """
        识别结果类型新增2
        """
        a = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[5][1])
        h = eval(DATA[5][2])
        d = eval(DATA[5][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[5][4]
        assert res.json()['code'] == DATA[5][5]

    def test_identify_type_delete(self, test_login):
        """
        识别结果类型删除
        """
        a = self.test_identify_type_list(test_login)
        u = ServerInfo.get_url(eval(DATA[6][1]))
        h = eval(DATA[6][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[6][4]
        assert res.json()['data'] == eval(DATA[6][5])



