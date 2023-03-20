import pytest
import yaml
import random
import allure
from config.config import ServerInfo
import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '项目管理', skip_first=True)

# with open(r'C:\Users\zj_001\PycharmProjects\system\data\test_tenant.yaml', 'r', encoding='utf-8') as f:
#     data = yaml.safe_load(f)


class TestProject:
    """
    项目管理
    """

    @allure.title('租户列表')
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

    @allure.title('租户对应的行业类型')
    def test_project_industry_class(self, test_login):
        """
        租户对应的行业类型
        """
        a = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        d = eval(DATA[1][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
        return res.json()['data'][-1]['id']

    @allure.title('获取项目类型')
    def test_project_class(self, test_login):
        """
        获取项目类型
        """
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        res = requests.get(url=u, headers=h)
        # print(res.json()['data'][0]['type'])
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]
        return res.json()['data'][0]['type']

    @allure.title('新增项目')
    def test_project_add(self, test_login):
        """
        新增项目
        """
        a = self.test_project_tenant_list(test_login)
        b = self.test_project_industry_class(test_login)
        c = self.test_project_class(test_login)
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        d = eval(DATA[3][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]
        return res.json()['data']['id']

    @allure.title('获取项目列表')
    def test_project_list(self, test_login):
        """
        获取项目列表
        """
        u = ServerInfo.get_url(DATA[4][1])
        h = eval(DATA[4][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]
        return res.json()['data']['list'][-1]['id'], res.json()['data']['list'][-1]['geo_workspace']

    @allure.title('修改项目')
    def test_project_update(self, test_login):
        """
        修改项目
        """
        a = self.test_project_tenant_list(test_login)
        b = self.test_project_industry_class(test_login)
        c = self.test_project_list(test_login)
        # print(c[0])
        u = ServerInfo.get_url(eval(DATA[5][1]))
        h = eval(DATA[5][2])
        d = eval(DATA[5][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[5][4]
        assert res.json()['code'] == DATA[5][5]

    @allure.title('删除项目')
    def test_project_delete(self, test_login):
        """
        删除项目
        """
        a = self.test_project_add(test_login)
        u = ServerInfo.get_url(eval(DATA[6][1]))
        h = eval(DATA[6][2])
        res = requests.delete(url=u, headers=h)
        # print(res.json())
        assert res.status_code == DATA[6][4]
        assert res.json()['code'] == DATA[6][5]

    @allure.title('分页查询')
    def test_project_query(self, test_login):
        """
        分页查询
        """
        a = self.test_project_tenant_list(test_login)
        u = ServerInfo.get_url(DATA[7][1])
        h = eval(DATA[7][2])
        d = eval(DATA[7][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.json()['code'] == DATA[7][4]
        assert res.status_code == DATA[7][5]

    @allure.title('识别结果类型名获取')
    def test_identify_type_list(self, test_login):
        """
        识别结果类型名获取
        """
        u = ServerInfo.get_url(DATA[8][1])
        h = eval(DATA[8][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[8][4]
        assert res.json()['code'] == DATA[8][5]
        return res.json()['data'][-1]['type_name'], res.json()['data'][-2]['type_name']

    @allure.title('建设目标新增')
    def test_project_build_add(self, test_login):
        """
        建设目标新增
        """
        a = self.test_project_tenant_list(test_login)
        b = self.test_project_list(test_login)[0]
        c = self.test_identify_type_list(test_login)[0]
        u = ServerInfo.get_url(DATA[9][1])
        h = eval(DATA[9][2])
        d = eval(DATA[9][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[9][4]
        assert res.json()['code'] == DATA[9][5]
        # return res.json()['data']['id']

    @allure.title('项目建设目标列表')
    def test_project_build_list(self, test_login):  # 必须列表中有数据才能单独运行，或在新增过后运行，不然下标会报错
        """
        项目建设目标列表
        """
        a = self.test_project_tenant_list(test_login)
        b = self.test_project_list(test_login)[0]
        u = ServerInfo.get_url(DATA[10][1])
        h = eval(DATA[10][2])
        d = eval(DATA[10][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[10][4]
        assert res.json()['code'] == DATA[10][5]
        return res.json()['data']['list'][-1]['id']

    @allure.title('项目建设修改')
    def test_project_build_update(self, test_login):  #list里必须有数据，才能单独运行
        """
        项目建设修改
        """
        a = self.test_project_tenant_list(test_login)
        b = self.test_project_list(test_login)[0]
        c = self.test_project_build_list(test_login)
        e = self.test_identify_type_list(test_login)[0]
        f = 1001
        u = ServerInfo.get_url(eval(DATA[11][1]))
        h = eval(DATA[11][2])
        d = eval(DATA[11][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[11][4]
        assert res.json()['data']['target'] == eval(DATA[11][5])

    @allure.title('建设目标新增1')
    def test_project_build_add2(self, test_login):
        """
        建设目标新增1
        """
        a = self.test_project_tenant_list(test_login)
        b = self.test_project_list(test_login)[0]
        c = self.test_identify_type_list(test_login)[1]
        u = ServerInfo.get_url(DATA[12][1])
        h = eval(DATA[12][2])
        d = eval(DATA[12][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[12][4]
        assert res.json()['code'] == DATA[12][5]

    @allure.title('项目建设删除')
    def test_project_build_delete(self, test_login):
        """
        项目建设删除
        """
        a = self.test_project_build_list(test_login)
        u = ServerInfo.get_url(eval(DATA[13][1]))
        h = eval(DATA[13][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[13][4]
        assert res.json()['data'] == eval(DATA[13][5])

    @allure.title('项目建设目标查询')
    def test_project_build_query(self, test_login):  # 必须列表中有数据才能单独运行，或在新增过后运行，不然下标会报错
        """
        项目建设目标查询
        """
        a = self.test_project_tenant_list(test_login)
        b = self.test_project_list(test_login)[0]
        u = ServerInfo.get_url(DATA[14][1])
        h = eval(DATA[14][2])
        d = eval(DATA[14][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[14][4]
        assert res.json()['code'] == DATA[14][5]