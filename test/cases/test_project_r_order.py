from config.config import ServerInfo

import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '订单管理', skip_first=True)

start_time = "2023-02-01"
end_time = "2023-02-28"

class TestOrder:
    """
    订单管理
    """

    def test_info(self, test_login2):
        """
        大屏用户信息
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        res = requests.get(url=u, headers=h)
        # print(res.json())
        assert res.status_code == DATA[0][4]
        assert res.json()['code'] == DATA[0][5]
        return res.json()['data']['tenant_id']

    def test_project_type(self, test_login2):
        """
        项目类型获取
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
        # print(res.json())
        return res.json()['data'][0]['type'], res.json()['data'][1]['type']   # 风能/光伏/房地产

    def test_periods_daterange(self, test_login2):
        """
        根据时间范围获取期数
        """
        u = ServerInfo.get_url(DATA[2][1])
        h = eval(DATA[2][2])
        d = eval(DATA[2][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[2][4]
        assert res.json()['code'] == DATA[2][5]
        return res.json()['data']

    def test_order_add(self, test_login2):
        """
        大屏新建订单(含关联模块)
        """
        a = self.test_project_type(test_login2)[0]
        b = self.test_periods_daterange(test_login2)
        u = ServerInfo.get_url(DATA[3][1])
        h = eval(DATA[3][2])
        d = eval(DATA[3][3])
        #  'data_period' 要与上一个用例 ’day‘一致；’data_period_type‘与上一个’type‘一致（week→W，month→M）
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[3][4]
        assert res.json()['code'] == DATA[3][5]
        return res.json()['data']['id'], res.json()['data']['associated_list'][0]['id']

    def test_order_add2(self, test_login2):
        """
        大屏创建订单（不含关联模块）
        """
        a = self.test_project_type(test_login2)[0]
        b = self.test_periods_daterange(test_login2)
        u = ServerInfo.get_url(DATA[4][1])
        h = eval(DATA[4][2])
        d = eval(DATA[4][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[4][4]
        assert res.json()['code'] == DATA[4][5]
        return res.json()['data']['id']

    def test_order_associated_add(self, test_login2):
        """
        新增关联模块（前提是订单里没有关联模块）
        """
        a = self.test_order_add2(test_login2)
        u = ServerInfo.get_url(eval(DATA[5][1]))
        h = eval(DATA[5][2])
        d = eval(DATA[5][3])
        res = requests.post(url=u, headers=h, json=d)
        assert res.status_code == DATA[5][4]
        assert res.json()['code'] == DATA[5][5]

    def test_order_list(self, test_login2):
        """
        大屏订单列表
        """
        u = ServerInfo.get_url(DATA[6][1])
        h = eval(DATA[6][2])
        res = requests.get(url=u, headers=h)
        # print(res.json())
        assert res.status_code == DATA[6][4]
        assert res.json()['code'] == DATA[6][5]
        return res.json()['data']['list'][0]['id']

    def test_order_detail(self, test_login2):
        """
        订单详情获取
        """
        a = self.test_order_add(test_login2)[0]
        # a = self.test_order_list(test_login2)
        u = ServerInfo.get_url(eval(DATA[7][1]))
        h = eval(DATA[7][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[7][4]
        assert res.json()['code'] == DATA[7][5]
        return res.json()['data']['associated_list'][0]['id']

    def test_order_update(self, test_login2):
        """
         订单基本信息修改
        """
        a = self.test_order_list(test_login2)
        b = self.test_periods_daterange(test_login2)
        c = self.test_project_type(test_login2)[1]
        u = ServerInfo.get_url(eval(DATA[8][1]))
        h = eval(DATA[8][2])
        d = eval(DATA[8][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[8][4]
        assert res.json()['code'] == DATA[8][5]

    def test_order_associated_update(self, test_login2):
        """
        订单关联模块修改
        """
        a = self.test_info(test_login2)
        b = self.test_order_add(test_login2)
        # b = self.test_order_list(test_login2)
        # c = self.test_order_detail(test_login2)
        u = ServerInfo.get_url(eval(DATA[9][1]))
        # print(u)
        h = eval(DATA[9][2])
        d = eval(DATA[9][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[9][4]
        assert res.json()['code'] == DATA[9][5]

    def test_order_associated_delete(self, test_login2):
        """
        订单关联模块删除
        """
        a = self.test_order_add(test_login2)
        u = ServerInfo.get_url(eval(DATA[10][1]))
        h = eval(DATA[10][2])
        res = requests.delete(url=u, headers=h)
        assert res.status_code == DATA[10][4]
        assert res.json()['data'] == eval(DATA[10][5])

    def test_order_put(self, test_login2):
        """
        订单提交
        """
        a = self.test_order_add2(test_login2)
        u = ServerInfo.get_url(eval(DATA[11][1]))
        h = eval(DATA[11][2])
        res = requests.put(url=u, headers=h)
        assert res.status_code == DATA[11][4]
        assert res.json()['code'] == DATA[11][5]
        return a

    def test_order_cancel_put(self, test_login2):
        """
        订单取消提交
        """
        a = self.test_order_put(test_login2)
        u = ServerInfo.get_url(eval(DATA[12][1]))
        h = eval(DATA[12][2])
        res = requests.put(url=u, headers=h)
        assert res.status_code == DATA[12][4]
        assert res.json()['code'] == DATA[12][5]

    def test_order_put1(self, test_login2):
        """
        订单再次提交
        """
        a = self.test_order_add2(test_login2)
        u = ServerInfo.get_url(eval(DATA[13][1]))
        h = eval(DATA[13][2])
        res = requests.put(url=u, headers=h)
        assert res.status_code == DATA[13][4]
        assert res.json()['code'] == DATA[13][5]

    def test_order_list2(self, test_login):
        """
        后台订单列表
        """
        u = ServerInfo.get_url(DATA[14][1])
        h = eval(DATA[14][2])
        res = requests.get(url=u, headers=h)
        assert res.json()['code'] == DATA[14][5]
        assert res.status_code == DATA[14][4]
        return res.json()['data']['list'][0]['id']

    def test_order_log(self, test_login):
        """
        订单日志查看
        """
        a = self.test_order_list2(test_login)
        u = ServerInfo.get_url(DATA[15][1])
        h = eval(DATA[15][2])
        d = eval(DATA[15][3])
        res = requests.get(url=u, headers=h, params=d)
        # print(res.url)
        assert res.status_code == DATA[15][4]
        assert res.json()['code'] == DATA[15][5]

    def test_order_type(self, test_login):
        """
        编辑里的类型获取
        """
        u = ServerInfo.get_url(DATA[16][1])
        h = eval(DATA[16][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[16][4]
        assert res.json()['code'] == DATA[16][5]

    def test_order_detail2(self, test_login):
        """
        后台订单详情
        """
        a = self.test_order_list2(test_login)
        u = ServerInfo.get_url(eval(DATA[17][1]))
        h = eval(DATA[17][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[17][4]
        assert res.json()['code'] == DATA[17][5]

    def test_order_list3(self, test_login):
        """
        后台订单列表获取(获取apply_state:1的第一条数据id)
        """
        u = ServerInfo.get_url(DATA[18][1])
        h = eval(DATA[18][2])
        res = requests.get(url=u, headers=h)
        a = res.json()['data']['list']
        # print(a[0]['id'])
        for item in a:
            if item['apply_state'] == 1:
                # print(item['id'])
                break
        assert res.status_code == DATA[18][4]
        assert res.json()['code'] == DATA[18][5]
        return item['id']

    def test_order_area_add(self, test_login):
        """
        后台订单增加关联地块
        """
        a = self.test_order_list3(test_login)
        u = ServerInfo.get_url(eval(DATA[19][1]))
        # print(a)
        h = eval(DATA[19][2])
        d = eval(DATA[19][3])
        res = requests.post(url=u, headers=h, json=d)
        # print(res.json())
        assert res.status_code == DATA[19][4]
        assert res.json()['code'] == DATA[19][5]

    def test_order_refuse(self, test_login):
        """
        审核拒绝
        """
        a = self.test_order_list3(test_login)
        # print(a)
        u = ServerInfo.get_url(eval(DATA[20][1]))
        h = eval(DATA[20][2])
        d = eval(DATA[20][3])
        res = requests.put(url=u, headers=h, json=d)
        assert res.status_code == DATA[20][4]
        assert res.json()['code'] == DATA[20][5]

    def test_order_pass(self, test_login):
        """
        审核通过
        """
        a = self.test_order_list3(test_login)
        u = ServerInfo.get_url(eval(DATA[21][1]))
        h = eval(DATA[21][2])
        res = requests.put(url=u, headers=h)
        assert res.status_code == DATA[21][4]
        assert res.json()['code'] == DATA[21][5]





