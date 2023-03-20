import allure
import pytest
import yaml
import requests
from config.config import ServerInfo
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '角色管理', skip_first=True)

# with open(r'C:\Users\zj_001\PycharmProjects\system\data\test_tenant.yaml', 'r', encoding='utf-8') as f:
#     data = yaml.safe_load(f)

class TestRole:
    """
    角色管理
    """

    @allure.title('租户列表')
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

    @allure.title('获取角色类型')
    def test_role_class(self, test_login):
        """
        获取角色类型
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        res = requests.get(url=u, headers=h)
        # print(res.json()['data'][0]['type'])
        assert res.json()['code'] == DATA[1][5]
        assert res.status_code == DATA[1][4]
        return res.json()['data'][0]['type'], res.json()['data'][1]['type']

    @allure.title('新增角色（管理员）')
    def test_role_add(self, test_login):
        """
        新增角色（管理员）
        """
        a = self.test_user_tenant(test_login)
        b = self.test_role_class(test_login)[0]
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        d = eval(DATA[2][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]
        return res.json()['data']['id']

    @allure.title('新增角色（普通用户）')
    def test_role_add1(self, test_login):
        """
        新增角色（普通用户）
        """
        a = self.test_user_tenant(test_login)
        b = self.test_role_class(test_login)[1]
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        d = eval(DATA[3][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]

    @allure.title('编辑角色')
    def test_role_update(self, test_login):
        """
        编辑角色
        """
        a = self.test_role_add(test_login)
        b = self.test_user_tenant(test_login)
        c = self.test_role_class(test_login)[1]
        u = ServerInfo.get_url(eval(DATA[4][1]))
        h = eval(DATA[4][2])
        d = eval(DATA[4][3])
        res = requests.put(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]

    @allure.title('获取角色列表')
    def test_role_list(self, test_login):
        """
        获取角色列表
        """
        u = ServerInfo.get_url(DATA[5][1])
        h = eval(DATA[5][2])
        res = requests.get(url=u, headers=h)
        # print(res.json()['data']['list'][-1]['id'])
        assert res.status_code == DATA[5][4]
        assert res.json()['code'] == DATA[5][5]
        return res.json()['data']['list'][-1]['id']

    @allure.title('删除角色')
    def test_role_delete(self, test_login):
        """
        删除角色
        """
        a = self.test_role_list(test_login)
        u = ServerInfo.get_url(eval(DATA[6][1]))
        h = eval(DATA[6][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[6][4]
        assert res.json()['code'] == DATA[6][5]

    @allure.title('分页查询')
    def test_role_query(self, test_login):
        """
        分页查询
        """
        a = self.test_user_tenant(test_login)
        u = ServerInfo.get_url(DATA[7][1])
        h = eval(DATA[7][2])
        d = eval(DATA[7][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[7][4]
        assert res.json()['code'] == DATA[7][5]

