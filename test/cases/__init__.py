import os

# case_path=os.path.dirname(os.path.abspath(__file__))
# print(case_path)

case_path = os.path.dirname(os.path.abspath(__file__))  # 当前路径
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 根路径
data_path = os.path.join(base_path, 'data')        #  拼接项目根路径下的任何路径

print(case_path, base_path, data_path)