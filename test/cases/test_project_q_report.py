import pytest
import yaml
import requests
from config.config import ServerInfo
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '图层报告', skip_first=True)

# with open(r'./../../data/test_tenant.yaml', 'r', encoding='utf-8') as f:
#     data = yaml.safe_load(f)

class TestLayerReport:
    """
    图层报告
    """

    def test_report_query(self, test_login):
        """
        图层报告分页查询
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        d = eval(DATA[0][3])
        res = requests.get(url=u, headers=h, params=d)
        assert res.json()['code'] == DATA[0][4]
        assert res.status_code == DATA[0][5]

    def test_project_class(self, test_login):
        """
        获取项目类型
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
        # print(res.json()['data'][-1]['id'])
        return res.json()['data'][-1]['id']

    def test_project_class_project(self, test_login):
        """
        项目类型对应的项目
        """
        a = self.test_project_class(test_login)
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        d = eval(DATA[2][3])
        res = requests.get(url=u, headers=h, params=d)
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]
        return res.json()['data'][-1]['id']

    def test_project_project_place(self, test_login):
        """
        项目对应的项目场所
        """
        a = self.test_project_class_project(test_login)
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        d = eval(DATA[3][3])
        res = requests.get(url=u, headers=h, params=d)
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]
        return res.json()['data'][-1]['id']

    def test_project_place_layer(self, test_login):
        """
        场所对应的图层
        """
        a = self.test_project_project_place(test_login)
        u = ServerInfo.get_url(DATA[4][1])
        h = eval(DATA[4][2])
        d = eval(DATA[4][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]
        return res.json()['data'][-1]['id']

    def test_report_files_upload(self, test_login):
        """
        文件上传(word)
        """
        u = ServerInfo.get_url(DATA[5][1])
        file = eval(DATA[5][3])
        h = eval(DATA[5][2])
        res = requests.post(url=u, files=file, headers=h)
        # print(res.json())
        assert res.status_code == DATA[5][4]
        assert res.json()['data']['filename'] == DATA[5][5]
        return res.json()['data']['id']

    def test_report_files_upload2(self, test_login):
        """
        文件上传(pdf)
        """
        u = ServerInfo.get_url(DATA[6][1])
        file = eval(DATA[6][3])
        h = eval(DATA[6][2])
        res = requests.post(url=u, files=file, headers=h)
        # print(res.json())
        assert res.status_code == DATA[6][4]
        assert res.json()['data']['filename'] == DATA[6][5]
        return res.json()['data']['id']

    def test_report_add(self, test_login):
        """
        添加报告(下载/word)
        """
        type = ["DOWNLOAD", "PREVIEW"]
        a = self.test_report_files_upload(test_login)
        b = self.test_project_place_layer(test_login)
        c = self.test_project_class(test_login)
        e = self.test_project_class_project(test_login)
        f = self.test_project_project_place(test_login)
        u = ServerInfo.get_url(DATA[7][1])
        h = eval(DATA[7][2])
        d = eval(DATA[7][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[7][4]
        assert res.json()['code'] == DATA[7][5]

    def test_report_add2(self, test_login):
        """
        添加报告(预览/pdf)
        """
        type = ["DOWNLOAD", "PREVIEW"]
        a = self.test_report_files_upload(test_login)
        b = self.test_project_place_layer(test_login)
        c = self.test_project_class(test_login)
        e = self.test_project_class_project(test_login)
        f = self.test_project_project_place(test_login)
        u = ServerInfo.get_url(DATA[8][1])
        h = eval(DATA[8][2])
        d = eval(DATA[8][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[8][4]
        assert res.json()['code'] == DATA[8][5]
        return res.json()['data']['id']

    def test_report_list(self, test_login):
        """
        报告列表
        """
        u = ServerInfo.get_url(DATA[9][1])
        h = eval(DATA[9][2])
        res = requests.get(url=u, headers=h)
        assert res.json()['code'] == DATA[9][4]
        assert res.status_code == DATA[9][5]
        return res.json()['data']['list'][-1]['id']

    def test_report_update(self, test_login):
        """
        修改报告
        """
        type = ["DOWNLOAD", "PREVIEW"]
        a = self.test_report_files_upload(test_login)
        b = self.test_project_place_layer(test_login)
        c = self.test_project_class(test_login)
        e = self.test_project_class_project(test_login)
        f = self.test_project_project_place(test_login)
        g = self.test_report_list(test_login)
        u = ServerInfo.get_url(eval(DATA[10][1]))
        h = eval(DATA[10][2])
        d = eval(DATA[10][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[10][4]
        assert res.json()['code'] == DATA[10][5]

    def test_report_delete(self, test_login):
        """
        删除报告
        """
        a = self.test_report_add2(test_login)
        u = ServerInfo.get_url(eval(DATA[11][1]))
        h = eval(DATA[11][2])
        res = requests.delete(url=u, headers=h)
        assert res.json()['data'] == eval(DATA[11][5])
        assert res.status_code == DATA[11][4]


