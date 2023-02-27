import pytest
import yaml
import random
import requests
from config.config import ServerInfo
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '用户管理', skip_first=True)


# with open(r'C:\Users\zj_001\PycharmProjects\system\data\test_tenant.yaml', 'r', encoding='utf-8') as f:
#     data = yaml.safe_load(f)
 # print(data)


class TestUser:
    """
    用户管理
    """

    def test_user_tenant(self, test_login):
        """
        租户列表
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        res = requests.get(url=u, headers=h)
        assert res.json()['code'] == DATA[0][5]
        assert res.status_code == DATA[0][4]
        return res.json()['data']['list'][-1]['id']

    def test_user_querylist(self, test_login):
        """
        分页查询
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        d = eval(DATA[1][3])
        res = requests.get(url=u, headers=h, params=d)
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]

    def test_user_add(self, test_login):
        """
        新增用户
        """
        c = random.randint(100000, 999999)
        e = str(c)
        a = self.test_user_tenant(test_login)
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        d = eval(DATA[2][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]
        return res.json()['data']['id']

    def test_user_update(self, test_login):
        """
        编辑用户
        """
        c = random.randint(100000, 999999)
        e = str(c)
        a = self.test_user_add(test_login)
        b = self.test_user_tenant(test_login)
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        d = eval(DATA[3][3])
        res = requests.put(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]

    def test_user_list(self, test_login):
        """
        用户列表
        """
        u = ServerInfo.get_url(DATA[4][1])
        h = eval(DATA[4][2])
        res = requests.get(url=u, headers=h)
        # print(res.json())
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]
        return res.json()['data']['list'][-1]['id']

    def test_user_delete(self, test_login):
        """
        删除用户
        """
        a = self.test_user_add(test_login)
        u = ServerInfo.get_url(eval(DATA[5][1]))
        h = eval(DATA[5][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[5][4]
        assert res.json()['data'] == eval(DATA[5][5])

    @pytest.mark.skip(reason='在角色里已运行用例')
    def test_role_add(self, test_login):
        """
        新增角色
        """
        a = self.test_user_tenant(test_login)
        u = ServerInfo.get_url(DATA[6][1])
        h = eval(DATA[6][2])
        d = eval(DATA[6][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[6][4]
        assert res.json()['code'] == DATA[6][5]

    def test_user_role_list(self, test_login):
        """
        用户对应的角色
        """
        a = self.test_user_tenant(test_login)
        b = self.test_user_list(test_login)
        u = ServerInfo.get_url(DATA[7][1])
        h = eval(DATA[7][2])
        d = eval(DATA[7][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.json()['code'] == DATA[7][5]
        assert res.status_code == DATA[7][4]
        return res.json()['data']['list'][0]['id'], res.json()['data']['list'][1]['id']

    def test_user_role_add(self, test_login):
        """
        用户添加角色(管理员)
        """
        a = self.test_user_list(test_login)
        b = self.test_user_role_list(test_login)[0]
        u = ServerInfo.get_url(DATA[8][1])
        h = eval(DATA[8][2])
        d = eval(DATA[8][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json()['data']['id'])
        assert res.json()['code'] == DATA[8][5]
        assert res.status_code == DATA[8][4]
        return res.json()['data']['id']

    def test_user_role_add1(self, test_login):
        """
        用户添加角色（普通用户）
        """
        a = self.test_user_list(test_login)
        b = self.test_user_role_list(test_login)[1]
        u = ServerInfo.get_url(DATA[9][1])
        h = eval(DATA[9][2])
        d = eval(DATA[9][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json()['data']['id'])
        assert res.json()['code'] == DATA[9][5]
        assert res.status_code == DATA[9][4]
        return res.json()['data']['id']

    def test_user_role_list1(self, test_login):
        """
        已用的用户角色列表（展示）
        """
        a = self.test_user_tenant(test_login)
        b = self.test_user_list(test_login)
        u = ServerInfo.get_url(DATA[10][1])
        h = eval(DATA[10][2])
        d = eval(DATA[10][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.json()['code'] == DATA[10][5]
        assert res.status_code == DATA[10][4]
        return res.json()['data']['list'][0]['id']

    def test_user_role_delete(self, test_login):
        """
        用户删除角色
        """
        a = self.test_user_role_list1(test_login)
        # print(a)
        u = ServerInfo.get_url(eval(DATA[11][1]))
        h = eval(DATA[11][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[11][4]
        assert res.json()['code'] == DATA[11][5]


