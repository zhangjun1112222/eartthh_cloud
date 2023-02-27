import pytest
import yaml
import random

from config.config import ServerInfo

import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '用户组管理', skip_first=True)

class TestUserGroup:
    """
    用户组管理
    """

    def test_project_tenant(self, test_login):
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

    def test_user_group_list(self, test_login):
        """
        获取用户组列表
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        res = requests.get(url=u, headers=h)
        # print(res.json()['data']['list'][-1]['id'])
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
        return res.json()['data']['list'][-1]['id']

    def test_user_group_add(self, test_login):
        """
        新增用户组
        """
        a = self.test_project_tenant(test_login)
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        d = eval(DATA[2][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]
        return res.json()['data']['id']

    def test_user_group_update(self, test_login):
        """
        编辑用户组
        """
        a = self.test_user_group_add(test_login)
        b = self.test_project_tenant(test_login)
        u = ServerInfo.get_url(eval(DATA[3][1]))
        h = eval(DATA[3][2])
        d = eval(DATA[3][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]

    def test_user_group_delete(self, test_login):
        """
        删除用户组
        """
        a = self.test_user_group_add(test_login)
        u = ServerInfo.get_url(eval(DATA[4][1]))
        h = eval(DATA[4][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[4][4]
        assert res.json()['data'] == eval(DATA[4][5])

    def test_tenant_to_user(self, test_login):
        """
        租户对应的用户数量
        """
        a = self.test_project_tenant(test_login)
        b = self.test_user_group_list(test_login)
        u = ServerInfo.get_url(DATA[5][1])
        h = eval(DATA[5][2])
        d = eval(DATA[5][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[5][4]
        assert res.json()['code'] == DATA[5][5]
        return res.json()['data']['list'][-1]['id']

    def test_user_group_user_list(self, test_login):
        """
        用户组对应的用户列表(展示)
        """
        a = self.test_project_tenant(test_login)
        b = self.test_user_group_list(test_login)
        u = ServerInfo.get_url(DATA[6][1])
        h = eval(DATA[6][2])
        d = eval(DATA[6][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.json()['code'] == DATA[6][4]
        assert res.status_code == DATA[6][5]

    def test_user_group_user_add(self, test_login):  # 同时两次单独调试会报错 ，同一用户不能添加两次
        """
        用户组里添加用户
        """
        a = self.test_user_group_list(test_login)
        b = self.test_tenant_to_user(test_login)
        u = ServerInfo.get_url(DATA[7][1])
        h = eval(DATA[7][2])
        d = eval(DATA[7][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[7][4]
        assert res.json()['data']['user_id'] == eval(DATA[7][5])

    def test_user_group_user_list1(self, test_login):  # 前提是必须先运行’用户组里添加用户‘，list才有数据 否则return 没有下标会报错
        """
        用户组对应的用户列表(展示)
        """
        a = self.test_project_tenant(test_login)
        b = self.test_user_group_list(test_login)
        u = ServerInfo.get_url(DATA[8][1])
        h = eval(DATA[8][2])
        d = eval(DATA[8][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.json()['code'] == DATA[8][4]
        assert res.status_code == DATA[8][5]
        return res.json()['data']['list'][-1]['id']

    def test_user_group_user_delete(self, test_login):  # list有数据才能进行删除调试
        """
        用户组里删除用户
        """
        a = self.test_user_group_user_list1(test_login)
        u = ServerInfo.get_url(eval(DATA[9][1]))
        h = eval(DATA[9][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[9][4]
        assert res.json()['code'] == DATA[9][5]

    def test_user_group_user_add1(self, test_login):  # 同时两次单独调试会报错 ，同一用户不能添加两次
        """
        用户组里重新添加用户
        """
        a = self.test_user_group_list(test_login)
        b = self.test_tenant_to_user(test_login)
        u = ServerInfo.get_url(DATA[10][1])
        h = eval(DATA[10][2])
        d = eval(DATA[10][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[10][4]
        assert res.json()['data']['user_id'] == eval(DATA[10][5])

    def test_user_group_project_group_list(self, test_login):
        """
        用户组里面对应的项目组（展示）
        """
        a = self.test_project_tenant(test_login)
        b = self.test_user_group_list(test_login)
        u = ServerInfo.get_url(DATA[11][1])
        h = eval(DATA[11][2])
        d = eval(DATA[11][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[11][4]
        assert res.json()['code'] == DATA[11][5]

    def test_tenant_to_project_group(self, test_login):
        """
        租户对应的项目组
        """
        a = self.test_project_tenant(test_login)
        b = self.test_user_group_list(test_login)
        u = ServerInfo.get_url(DATA[12][1])
        h = eval(DATA[12][2])
        d = eval(DATA[12][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.text)
        assert res.status_code == DATA[12][4]
        assert res.json()['code'] == DATA[12][5]
        return res.json()['data']['list'][-1]['id']

    def test_user_group_project_group_add(self, test_login):  # 必须有对应的项目组，且不能单独调试两次
        """
        用户组添加项目组
        """
        a = self.test_tenant_to_project_group(test_login)
        b = self.test_user_group_list(test_login)
        u = ServerInfo.get_url(DATA[13][1])
        h = eval(DATA[13][2])
        d = eval(DATA[13][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[13][4]
        assert res.json()['code'] == DATA[13][5]

    def test_user_group_project_group_list1(self, test_login):  # 前提是必须先运行’用户组添加项目组‘，list才有数据 否则return 没有下表会报错
        """
        用户组里面对应的项目组（展示）
        """
        a = self.test_project_tenant(test_login)
        b = self.test_user_group_list(test_login)
        u = ServerInfo.get_url(DATA[14][1])
        h = eval(DATA[14][2])
        d = eval(DATA[14][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[14][4]
        assert res.json()['code'] == DATA[14][5]
        return res.json()['data']['list'][-1]['id']

    def test_user_group_project_group_delete(self, test_login):  # 必须list有项目组，且不能单独调试两次
        """
        用户组里删除项目组
        """
        a = self.test_user_group_project_group_list1(test_login)
        u = ServerInfo.get_url(eval(DATA[15][1]))
        h = eval(DATA[15][2])
        res = requests.delete(url=u, headers=h)
        # print(res.json())
        assert res.status_code == DATA[15][4]
        assert res.json()['code'] == DATA[15][5]

    def test_user_group_project_group_add1(self, test_login):  # 必须有对应的项目组，且不能单独调试两次
        """
        用户组重新添加项目组
        """
        a = self.test_tenant_to_project_group(test_login)
        b = self.test_user_group_list(test_login)
        u = ServerInfo.get_url(DATA[16][1])
        h = eval(DATA[16][2])
        d = {'project_group_id': a, 'user_group_id': b}
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[16][4]
        assert res.json()['code'] == DATA[16][5]


