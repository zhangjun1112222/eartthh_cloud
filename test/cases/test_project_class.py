from config.config import ServerInfo

import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '项目类型管理', skip_first=True)


class TestProjectClass:
    """
    项目类型管理
    """
    def test_tenant(self, test_login):
        """
        租户列表
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[0][4]
        assert res.json()['code'] == DATA[0][5]
        return res.json()['data'][-1]['id']

    def test_project_class_add(self, test_login):
        """
        新增项目类型
        """
        a = self.test_tenant(test_login)
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        d = eval(DATA[1][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
        return res.json()['data']['id']

    def test_project_class_list(self, test_login):
        """
        项目类型分页获取
        """
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        res = requests.get(url=u, headers=h)
        # print(res.json())
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]

    def test_project_class_query(self, test_login):
        """
        项目类型分页查询获取
        """
        a = self.test_tenant(test_login)
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        d = eval(DATA[3][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.url)
        # print(res.json())
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]

    def test_project_class_update(self,test_login):
        """
        修改项目类型
        """
        a = self.test_project_class_add(test_login)
        u = ServerInfo.get_url(eval(DATA[4][1]))
        h = eval(DATA[4][2])
        d = eval(DATA[4][3])
        res = requests.put(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[4][4]
        assert res.json()['data']['name'] == DATA[4][5]

    def test_project_class_delete(self, test_login):
        """
        删除项目类型
        """
        a = self.test_project_class_add(test_login)
        u = ServerInfo.get_url(eval(DATA[5][1]))
        h = eval(DATA[5][2])
        res = requests.delete(url=u, headers=h)
        # print(res.json())
        assert res.status_code == DATA[5][4]
        assert res.json()['data'] == eval(DATA[5][5])

