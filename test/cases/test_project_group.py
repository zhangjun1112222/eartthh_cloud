import pytest
import yaml
import random

from config.config import ServerInfo

import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '项目组管理', skip_first=True)

# with open(r'C:\Users\zj_001\PycharmProjects\system\data\test_tenant.yaml', 'r', encoding='utf-8') as f:
#     data = yaml.safe_load(f)


class TestProjectGroup:
    """
    项目组管理
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

    def test_project_group_add(self, test_login):
        """
        新增项目组
        """
        a = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        d = eval(DATA[1][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
        return res.json()['data']['id']

    def test_project_group_update(self, test_login):
        """
        修改项目组
        """
        a = self.test_project_tenant_list(test_login)
        b = self.test_project_group_add(test_login)
        u = ServerInfo.get_url(eval(DATA[2][1]))
        h = eval(DATA[2][2])
        d = eval(DATA[2][3])
        res = requests.put(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]

    def test_project_group_list(self, test_login):
        """
        获取项目组列表
        """
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]
        # print(res.json()['data']['list'][-1]['id'])
        return res.json()['data']['list'][-1]['id']

    def test_project_group_delete(self, test_login):
        """
        删除项目组
        """
        a = self.test_project_group_list(test_login)
        u = ServerInfo.get_url(eval(DATA[4][1]))
        h = eval(DATA[4][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]

    def test_tenant_project_list(self, test_login):
        """
        租户对应的所有项目
        """
        a = self.test_project_group_list(test_login)
        b = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[5][1])
        h = eval(DATA[5][2])
        d = eval(DATA[5][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json()['data']['list'][-1])
        assert res.status_code == DATA[5][4]
        assert res.json()['code'] == DATA[5][5]
        return res.json()['data']['list'][-1]['id']  # 返回的项目id

    def test_group_project_add(self, test_login):  # 只能单独调试一次
        """
        项目组里添加项目
        """
        tenant_id = self.test_project_tenant_list(test_login)
        project_group_id = self.test_project_group_list(test_login)
        project_id = self.test_tenant_project_list(test_login)
        # print(tenant_id,project_group_id,project_id)
        u = ServerInfo.get_url(DATA[6][1])
        h = eval(DATA[6][2])
        d = eval(DATA[6][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[6][4]
        assert res.json()['code'] == DATA[6][5]
        # return res.json()['data']['id']

    def test_group_project_list(self, test_login):
        """
        项目组里面项目列表(展示) # 必须先运行 test_group_project_add，不然单独运行没有数据 list为空不能取下标
        """
        a = self.test_project_group_list(test_login)
        b = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[7][1])
        h = eval(DATA[7][2])
        d = eval(DATA[7][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json()['data']['list'][0]['id'])
        assert res.status_code == DATA[7][4]
        assert res.json()['code'] == DATA[7][5]
        return res.json()['data']['list'][0]['id']

    def test_group_project_delete(self, test_login):
        """
        项目组里删除项目 # 必须新增过后才能进行删除，单独运行没有参数会报错
        """
        # a = self.test_group_project_add(test_login)
        b = self.test_group_project_list(test_login)
        u = ServerInfo.get_url(eval(DATA[8][1]))
        h = eval(DATA[8][2])
        res = requests.delete(url=u, headers=h)
        # print(res.json())
        assert res.json()['code'] == DATA[8][4]
        assert res.status_code == DATA[8][5]

    def test_group_project_add1(self, test_login):  # 只能单独调试一次
        """
        项目组里重新添加项目
        """
        tenant_id = self.test_project_tenant_list(test_login)
        project_group_id = self.test_project_group_list(test_login)
        project_id = self.test_tenant_project_list(test_login)
        # print(tenant_id,project_group_id,project_id)
        u = ServerInfo.get_url(DATA[9][1])
        h = eval(DATA[9][2])
        d = eval(DATA[9][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[9][4]
        assert res.json()['code'] == DATA[9][5]


