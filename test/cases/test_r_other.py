import pytest

from config.config import ServerInfo

import requests
from test.cases import case_path, data_path
from utils.exceltools import ExcelTools
DATA = ExcelTools.read_excel(f'{data_path}/用例数据.xls', '其他接口', skip_first=True)

class TestOther:
    """
    其他接口
    """
    def test_newest(self, test_login):
        """
        用户最新通知
        """
        u = ServerInfo.get_url(DATA[0][1])
        h = eval(DATA[0][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[0][4]
        assert res.json()['code'] == DATA[0][5]

    @pytest.mark.skip(reason='404')
    def test_health(self, test_login):
        """
        健康检查
        """
        u = ServerInfo.get_url(DATA[1][1])
        h = eval(DATA[1][2])
        res = requests.get(url=u, headers=h)
        assert res.status_code == DATA[1][4]
        assert res.json()['code'] == DATA[1][5]
