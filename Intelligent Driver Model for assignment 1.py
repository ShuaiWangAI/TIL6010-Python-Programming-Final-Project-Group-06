import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import math
import time
import numpy as np
mpl.rcParams['axes.unicode_minus'] = False
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

path = 'E:/zuoye/assignment1/assignment1/data/filtered data/new_id/id 45.csv'

xdata1 = []
# Read csv file using pandas library under python
data = pd.read_csv(path)

ydata1 = data['kp']            # vehicle location
ydata_preceding = data['leader_kp']   # front car position
length_preceding = data['leader_length']  # Front car length
v_preceding=data['leader_velocity']/3.6  # Speed of the car ahead

for i in range(len(ydata1)):
    xdata1.append(0.1 * i)
error = []
T_temp = []

# starting IDM

S = 3.897155762  # static distance
T = 0.81  # headway
aMax = 2.445007324  # maximum expected acceleration
bMax = 1.039291382 # maximum expected deceleration
V0 = 26.25274658  # m/s Desired free flow velocity
reaction_time = 5  # Reaction time
xVelocity = data['velocity']/3.6    # km/h to m/s
V = [0 for i in range(len(xdata1))]     # measured vehicle speed
A = [0 for i in range(len(xdata1))]     # measured vehicle acceleration
V[0 + reaction_time] = xVelocity[0 + reaction_time]     
ydata_yuce = [0 for i in range(len(xdata1))]        # predicted vehicle position
ydata_yuce[0 + reaction_time] = ydata1[0 + reaction_time]

# Predict vehicle position with time as a loop
for i in range(len(xdata1) - 1 - reaction_time):
    canshu1 = (V[i + reaction_time] / V0)
    canshu2 = S + V[i + reaction_time] * T + (
                V[i + reaction_time] * (V[i + reaction_time] - v_preceding[i]) / 2 * ((aMax * bMax) ** 0.5))
    canshu3 = ydata_preceding[i] - length_preceding[i] - ydata_yuce[i + reaction_time]
    A[i + reaction_time] = aMax * (1 - canshu1 ** 4 - (canshu2 / canshu3) ** 2)
    V[i + 1 + reaction_time] = V[i + reaction_time] + A[i + reaction_time] * 0.1
    if ydata1[0] < ydata1[5]:
        ydata_yuce[i + 1 + reaction_time] = ydata_yuce[i + reaction_time] + 0.5 * A[
            i + reaction_time] * 0.1 ** 2 + V[i + reaction_time] * 0.1
    else:
        ydata_yuce[i + 1 + reaction_time] = ydata_yuce[i + reaction_time] - 0.5 * A[
            i + reaction_time] * 0.1 ** 2 - V[i + reaction_time] * 0.1

ydata_yuce_temp = ydata_yuce[reaction_time:-reaction_time]
V_temp = V[reaction_time:-reaction_time]
A_temp = A[reaction_time:-reaction_time]

ydata_preceding_temp = ydata_preceding[reaction_time:-reaction_time]    # measured front car position
ydata1_temp = ydata1[reaction_time:-reaction_time]     # predicted car position
xdata1_temp = xdata1[reaction_time:-reaction_time]     # time


c={"Velocity" : V_temp,
   "Acceleration" : A_temp,
    "front car position":ydata_preceding_temp,
     "following car position" :  ydata1_temp,
     "time":xdata1_temp
   }#将列表a，b转换成字典
data2=DataFrame(c)
print(data2)
data2.to_csv('E:/zuoye/IDMdata/IDMdata_for_45.csv')
#print(ydata_preceding_temp)
# def Fig():

#     plt.figure('The difference between measured and predicted trajectories')
#     plt.plot(xdata1_temp, ydata1_temp, label='Measured_car')
#     plt.plot(xdata1_temp, ydata_preceding_temp, label='Preceding_car')
#     # plt.plot(xdata1_temp, V_temp, label='Predicting_car',color='r')
#     # plt.plot(S, error, label='Predicting_car')
#     plt.title(u"id 751 Variation=9.99", size=30)
#     plt.legend(fontsize=25)
#     plt.xlabel(u't(s)', size=30)
#     plt.ylabel(u'x(m)', size=30)
#     plt.tick_params(labelsize=23)
#     # plt.savefig('C:\\Users\\yangyukuan\\Desktop\\data_nyj\\12.11\\cte误差.jpg')
#     plt.show()
#     print("all picture is starting")


# Fig()
