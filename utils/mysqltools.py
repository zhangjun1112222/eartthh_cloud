import pymysql

class MysqlTools():
    def __init__(self, host='', port='', user='', password='', db=''):
        self.db = db
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connect = self.get_db_connnect()

    # 创建连接并且
    def get_db_connnect(self):
        return pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)

    # 获取游标
    def get_db_cursor(self):
        return self.connect.cursor()

    # 执行sql语句
    def query(self, sql):
        cur = self.get_db_cursor()
        cur.execute(sql)
        return cur.fetchall()

    # 关闭数据库连接
    def __del__(self):
        # 当类结束的时候，会自动调用这个方法，析构方法
        self.connect.close()

if __name__ == "__main__":
    mysql_tools = MysqlTools()
    res = mysql_tools.query('select * from t_user where username ="liuyun1"')
    print(res)



# # 1.连接数据库
# DBCONFIG = {
#     "host":"ljtest.liuyun.tech",
#     "port":33306,
#     "user":"root",
#     "password":"1qaz!QAZ",
#     "db":"ljtestdb"
# }

# # sql语句要注意内双外单，内单外双的原则
# sql = "select * from t_user where username = 'liuyun1'"
# # 连接并且打开数据库
# db = pymysql.connect(host=DBCONFIG["host"], port=DBCONFIG["port"], user=DBCONFIG['user'], password=DBCONFIG['password'], db=DBCONFIG["db"])
# # 获取查询窗口：游标
# cur = db.cursor()
# # 通过查询窗口执行sql语句
# cur.execute(sql)
# # 获取查询对应的结果
# res = cur.fetchall()
# # 关闭数据库连接
# db.close()

# # 如果查询的结果为空，返回值就是(), 长度> 0
# # 如果查询的结果不为空，返回值((row1), (row2), (row3))> 长度不为0
# print(res)
# print(len(res))


