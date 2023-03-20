import pytest
import yaml
import random
import allure
from config.config import ServerInfo

import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '卫星历史图层', skip_first=True)

# with open(r'C:\Users\zj_001\PycharmProjects\system\data\test_tenant.yaml', 'r', encoding='utf-8') as f:
#     data = yaml.safe_load(f)

class TestProjectLayer:
    """
    卫星历史图层
    """

    @allure.title('图层分页查询 ')
    def test_layer_list(self, test_login):
        """
        图层分页查询
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        d = eval(DATA[0][3])
        res = requests.get(url=u, headers=h, params=d)
        assert res.status_code == DATA[0][4]
        assert res.json()['code'] == DATA[0][5]

    @allure.title('获取项目类型 ')
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

    @allure.title('项目类型对应的项目 ')
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

    @allure.title('项目对应的项目场所 ')
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

    @allure.title('图片上传 ')
    def test_picture_upload(self, test_login):
        """
        图片上传
        """
        u = ServerInfo.get_url(DATA[4][1])
        file = eval(DATA[4][3])
        h = eval(DATA[4][2])
        res = requests.post(url=u, headers=h, files=file)
        # print(res.json())
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]
        return res.json()['data']['id']

    @allure.title('图层上传 ')
    def test_layer_upload(self, test_login):
        """
        图层上传
        """
        a = self.test_picture_upload(test_login)
        b = self.test_project_class(test_login)
        c = self.test_project_class_project(test_login)
        e = self.test_project_project_place(test_login)
        u = ServerInfo.get_url(DATA[5][1])
        h = eval(DATA[5][2])
        d = eval(DATA[5][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.json()['code'] == DATA[5][4]
        assert res.status_code == DATA[5][5]
        return res.json()['data']['id'], res.json()['data']['attachment_id'], res.json()['data']['geo_layer'], res.json()['data']['geo_workspace'], res.json()['data']['project_id'], res.json()['data']['project_place_id']

    @allure.title('图层修改 ')
    def test_layer_update(self, test_login):
        """
        图层修改
        """
        a = self.test_layer_upload(test_login)
        # print(a)
        b = self.test_picture_upload(test_login)
        c = self.test_project_class(test_login)
        u = ServerInfo.get_url(eval(DATA[6][1]))
        h = eval(DATA[6][2])
        d = eval(DATA[6][3])
        res = requests.put(url=u, headers=h, json=d)
        # print(res.json())
        assert res.json()['code'] == DATA[6][4]
        assert res.status_code == DATA[6][5]

    @allure.title('图层删除 ')
    def test_layer_delete(self, test_login):
        """
        图层删除
        """
        a = self.test_layer_upload(test_login)[0]
        u = ServerInfo.get_url(eval(DATA[7][1]))
        h = eval(DATA[7][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[7][4]
        assert res.json()['data'] == eval(DATA[7][5])

    @allure.title('图层列表 ')
    def test_layer_list2(self, test_login):
        """
        图层列表
        """
        u = ServerInfo.get_url(DATA[8][1])
        h = eval(DATA[8][2])
        res = requests.get(url=u, headers=h)
        assert res.json()['code'] == DATA[8][5]
        assert res.status_code == DATA[8][4]
        return res.json()['data']['list'][-1]['id']

    @allure.title('重新生成功能 ')
    @pytest.mark.skip(reason='报错')
    def test_layer_rebuild(self, test_login):
        """
        重新生成功能
        """
        a = self.test_layer_list2(test_login)
        u = ServerInfo.get_url(DATA[9][1])
        h = eval(DATA[9][2])
        d = eval(DATA[9][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == 200
        assert res.json()['code'] == 200
