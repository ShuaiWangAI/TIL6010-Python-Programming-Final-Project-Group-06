import geatpy as ea
import numpy as np
import pandas as pd
import math
np.set_printoptions(suppress=True)
import csv
import matplotlib.pyplot as plt
import pandas as pd
import os

#path = 'E:/毕业论文/dataset/highd-dataset-v1.0/筛选数据个数大于750frame_匹配/35_car - 副本'
path = 'F:/2 TUD/1 First Year/Q1/Python/Project/assignment1/data/raw data/id'
all_canshu = []

def get_file():  # Create an empty list
    files = os.listdir(path)
    files.sort()  # sort
    list = []
    for file in files:
        if not os.path.isdir(path + file):  # Determine if the file is a folder
            f_name = str(file)
            #             print(f_name)
            tr = '/'  # add an extra slash
            filename = path + tr + f_name
            list.append(filename)
    return list


list = get_file()
for name in range(len(list)):
    data_ori = pd.read_csv(list[name])
    id_rear = data_ori.iloc[1, 1]  # vehicle number
    length_rear = data_ori.iloc[1, 4]  # rear length
    height_rear = data_ori.iloc[1, 5]  # rear width
    front_width = data_ori.iloc[1,23]  # Front car length
    print(front_width)
    r = 1  # Additional data needed by the objective function
    @ea.Problem.single
    def evalVars(Vars):  # Define the objective function (with constraints)
        S = Vars[0]  # 静态车间距 Expected headway
        T = Vars[1]  # 车头时距 Expected time headway
        aMax = Vars[2]  # 最大期望加速度 Maximum expected acceleration
        bMax = Vars[3]  # 最大期望减速度 Maximum expected deceleration
        V0 = Vars[4]  # m/s 期望自由流速度 Free flow speed

        path = list[name]

        xdata1 = []
        # Read csv file using pandas library under python
        data = pd.read_csv(path)

        ydata1 = data['x']  # 车辆位置 measured car position
        ydata_preceding = data['preceding_x']  # 前车位置 front car position
        length_preceding = data['front_width']  # 前车长度 Front car length
        v_preceding = data['precedingXVelocity']  # 前车速度 Speed of the car ahead

        for i in range(len(ydata1)):
            xdata1.append(0.04 * i)

        # start
        reaction_time = 20
        xVelocity = data['xVelocity']
        V = [0 for i in range(len(xdata1))]
        A = [0 for i in range(len(xdata1))]
        V[0 + reaction_time] = xVelocity[0 + reaction_time]
        ydata_yuce = [0 for i in range(len(xdata1))]  # predicting car position
        ydata_yuce[0 + reaction_time] = ydata1[0 + reaction_time]
        for i in range(len(xdata1) - 1 - reaction_time):
            canshu1 = (V[i + reaction_time] / V0)
            canshu2 = S + V[i + reaction_time] * T + (
                    V[i + reaction_time] * (V[i + reaction_time] - v_preceding[i]) / 2 * ((aMax * bMax) ** 0.5))
            canshu3 = ydata_preceding[i] - length_preceding[i] - ydata_yuce[i + reaction_time]
            A[i + reaction_time] = aMax * (1 - canshu1 ** 4 - (canshu2 / canshu3) ** 2)
            V[i + 1 + reaction_time] = V[i + reaction_time] + A[i + reaction_time] * 0.04
            if ydata1[0] < ydata1[5]:
                ydata_yuce[i + 1 + reaction_time] = ydata_yuce[i + reaction_time] + 0.5 * A[i + reaction_time] * 0.04 ** 2 + \
                                                    V[i + reaction_time] * 0.04
            else:
                ydata_yuce[i + 1 + reaction_time] = ydata_yuce[i + reaction_time] - 0.5 * A[i + reaction_time] * 0.04 ** 2 - \
                                                    V[i + reaction_time] * 0.04
        ydata_yuce = ydata_yuce[reaction_time:-reaction_time]
        ydata_preceding = ydata_preceding[reaction_time:-reaction_time]
        ydata1 = ydata1[reaction_time:-reaction_time]
        xdata1 = xdata1[reaction_time:-reaction_time]
        # done
        f = np.sum((ydata1 - ydata_yuce) ** 2)  # 计算目标函数值 Calculate the objective function value
        return f


    problem = ea.Problem(name='soea quick start demo',
                         M=1,  # 目标维数 target dimension
                         maxormins=[1],  # 目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标 target min-maximization flag list, 1: minimize this target; -1: maximize this target
                         Dim=5,  # 决策变量维数 decision variable dimension
                         varTypes=[0, 0, 0, 0, 0],  # 决策变量的类型列表，0：实数；1：整数 List of types of decision variables, 0: real; 1: integer
                         lb=[1, 0.5, 0.5, 0.5, 0],  # 决策变量下界 decision variable lower bound
                         ub=[8, 5, 6, 6, 50],  # 决策变量上界 decision variable upper bound
                         evalVars=evalVars)
    # 构建算法
    algorithm = ea.soea_SEGA_templet(problem,
                                     ea.Population(Encoding='RI', NIND=20),
                                     MAXGEN=50,  # 最大进化代数 maximum evolutionary algebra
                                     logTras=1,  # 表示每隔多少代记录一次日志信息，0表示不记录 Indicates how many generations to record log information, 0 means not to record
                                     trappedValue=1e-6,  # 单目标优化陷入停滞的判断阈值 Judgment threshold for stalled single-objective optimization
                                     maxTrappedCount=10)  # 进化停滞计数器最大上限值 Evolutionary stagnation counter maximum upper limit value
    # 求解
    res = ea.optimize(algorithm, seed=None, verbose=True, drawing=0, outputMsg=True, drawLog=False, saveFlag=True,
                      dirName='result')
    canshu = np.append(res['Vars'], res['ObjV'])
    canshu_list = canshu.tolist()
    canshu_list.append(id_rear)
    canshu_list.append(length_rear)
    canshu_list.append(height_rear)
    canshu_list.append(front_width)
    all_canshu.append(canshu_list)

# print(all_canshu)
# canshu_list = np.array(canshu_list).reshape(len(list),10)
df_info = pd.DataFrame(all_canshu,columns=['S','T','aMax','bMax','v0','least square','id','length','width','front_width'])
df_info.to_csv('E:/毕业论文/dataset/highd-dataset-v1.0/筛选数据个数大于750frame_匹配/35_car - 副本/10_canshu.csv', mode='a', index=0)

# print(canshu_list)
# print(info, "处理完")
# print('\n')