from config.config import ServerInfo

import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '识别结果管理', skip_first=True)

class TestIdentifyResult:
    """
    识别结果管理
    """

    def test_result_query(self, test_login):
        """
        识别结果分页查询
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        d = eval(DATA[0][3])
        res = requests.get(url=u, headers=h, params=d)
        assert res.json()['code'] == DATA[0][4]
        assert res.status_code == DATA[0][5]

    def test_project_class_list(self, test_login):
        """
        获取项目类型
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
        return res.json()['data'][-1]['id']

    def test_result_type(self, test_login):
        """
        获取结果类型
        """
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]
        return res.json()['data'][0]['type'], res.json()['data'][1]['type']   # 高度 / 常规

    def test_type_name(self, test_login):
        """
        获取类型名
        """
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][4]
        # print(res.json())
        return res.json()['data'][-1]['type_name'], res.json()['data'][-2]['type_name']  # 最后2个类型名不能同名

    def test_identify_unit(self, test_login):
        """
        获取识别单位
        """
        u = ServerInfo.get_url(DATA[4][1])
        h = eval(DATA[4][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]
        # print(res.json())
        return res.json()['data'][-1]['identify_unit']

    def test_class_project(self, test_login):
        """
        项目类型对应的项目
        """
        a = self.test_project_class_list(test_login)
        u = ServerInfo.get_url(DATA[5][1])
        h = eval(DATA[5][2])
        d = eval(DATA[5][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[5][4]
        assert res.json()['code'] == DATA[5][5]
        return res.json()['data'][-1]['id']

    def test_project_to_place(self, test_login):
        """
        项目对应的场所
        """
        a = self.test_class_project(test_login)
        u = ServerInfo.get_url(DATA[6][1])
        h = eval(DATA[6][2])
        d = eval(DATA[6][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[6][4]
        assert res.json()['code'] == DATA[6][5]
        return res.json()['data'][-1]['id']

    def test_place_to_layer(self, test_login):
        """
        场所对应的图层
        """
        a = self.test_project_to_place(test_login)
        u = ServerInfo.get_url(DATA[7][1])
        h = eval(DATA[7][2])
        d = eval(DATA[7][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.json())
        assert res.status_code == DATA[7][4]
        assert res.json()['code'] == DATA[7][5]
        return res.json()['data'][-1]['id']

    def test_result_upload(self, test_login):
        """
        上传文件
        """
        file = eval(DATA[8][3])
        u = ServerInfo.get_url(DATA[8][1])
        h = eval(DATA[8][2])
        res = requests.post(url=u, files=file, headers=h)
        # print(res.json())
        assert res.status_code == DATA[8][4]
        assert res.json()['code'] == DATA[8][5]
        return res.json()['data']['id']

    def test_result_add(self, test_login):
        """
        识别结果新增
        """
        a = self.test_identify_unit(test_login)
        b = self.test_result_upload(test_login)
        c = self.test_place_to_layer(test_login)
        e = self.test_project_class_list(test_login)
        f = self.test_class_project(test_login)
        g = self.test_project_to_place(test_login)
        i = self.test_result_type(test_login)[-1]
        j = self.test_type_name(test_login)[0]
        u = ServerInfo.get_url(DATA[9][1])
        h = eval(DATA[9][2])
        d = eval(DATA[9][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[9][4]
        assert res.json()['code'] == DATA[9][5]

    def test_result_list(self, test_login):
        """
        识别结果列表
        """
        u = ServerInfo.get_url(DATA[10][1])
        h = eval(DATA[10][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[10][4]
        assert res.json()['code'] == DATA[10][5]
        return res.json()['data']['list'][-1]['id']

    def test_result_update(self, test_login):
        """
        识别结果修改
        """
        a1 = self.test_result_list(test_login)
        a = self.test_identify_unit(test_login)
        b = self.test_result_upload(test_login)
        c = self.test_place_to_layer(test_login)
        e = self.test_project_class_list(test_login)
        f = self.test_class_project(test_login)
        g = self.test_project_to_place(test_login)
        i = self.test_result_type(test_login)[-2]
        j = self.test_type_name(test_login)[0]
        u = ServerInfo.get_url(eval(DATA[11][1]))
        h = eval(DATA[11][2])
        d = eval(DATA[11][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[11][4]
        assert res.json()['code'] == DATA[11][5]

    def test_result_add2(self, test_login):   # 再次新增获取最后2个类型名不能相同，否则报错
        """
        识别结果新增
        """
        a = self.test_identify_unit(test_login)
        b = self.test_result_upload(test_login)
        c = self.test_place_to_layer(test_login)
        e = self.test_project_class_list(test_login)
        f = self.test_class_project(test_login)
        g = self.test_project_to_place(test_login)
        i = self.test_result_type(test_login)[-1]
        j = self.test_type_name(test_login)[1]
        u = ServerInfo.get_url(DATA[12][1])
        h = eval(DATA[12][2])
        d = eval(DATA[12][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[12][4]
        assert res.json()['code'] == DATA[12][5]

    def test_result_delete(self, test_login):
        """
        识别结果删除
        """
        a = self.test_result_list(test_login)
        u = ServerInfo.get_url(eval(DATA[13][1]))
        h = eval(DATA[13][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[13][4]
        assert res.json()['data'] == eval(DATA[13][5])
