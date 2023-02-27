import xlrd


class ExcelTools():

    @staticmethod
    def read_excel(excel_path, sheet_name, skip_first=True):
        """
            方法：python读取excel
            参数：
                excel_path：excel的路径
                sheet_name：sheet页面的名字
                skip_first: 是否跳过首行：True
            返回值：
                [
                    [1, "查询所有病例报告", "/haimo/sass/cases/sassListCase/10/1","{}", '{"token": user_login}', 200, 1],
                    [行2],
                    [行3]..
                ]
        """
        results = []

        datas = xlrd.open_workbook(excel_path)  # 打开excel
        table = datas.sheet_by_name(sheet_name)  # 打开对应页面的sheet
        if skip_first is True:
            start_row = 1  # 0是第一行，1是第二行开始
        else:
            start_row = 0

        # 循环读取每一行数据
        for row in range(start_row, table.nrows):  # range(1, 4) > [1,2,3]
            results.append(table.row_values(row))

        return results


if __name__ == "__main__":
    a = ExcelTools.read_excel(r'C:\Users\zj_001\Desktop\新建 XLS 工作表.xls', 'Sheet1', skip_first=True)
    print(a)

    # [
    #     [1.0, '查询所有病例报告', '/haimo/sass/cases/sassListCase/10/1', '{}', '{"token": user_login}', 200.0, 1.0],
    #     [2.0, '查看所有医院', '/haimo/sass/hospital/release/listEffectiveHospital', '', '{"token": user_login}', 200.0, 1.0],
    #     [3.0, '搜索病例', '/haimo/sass/cases/sassListCase/10/1', '[{"patientName":""}, {"patientName":"","phone":"13888889999"}, {"patientName":"","phone":"","gender":1}]', '{"token": user_login}', 200.0, 1.0]
    # ]