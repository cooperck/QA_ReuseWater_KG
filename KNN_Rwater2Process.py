# # 定义一个KNN从输入的水质数据找出返回对应的工程名称
# # 输入数据格式为{'recovery': '70', 'quantity': '200', 'CI_in': '1500'，……}
# # 数据关键词有：'quantity'，'recovery'，'COD_in'，'CI_in'，'Hardness_in'，'ss_in'
# # 要求返回结果为{'project'：[‘项目名称’]}

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from sklearn.neighbors import KNeighborsClassifier
from numpy import *

class KNN_Water2Process:
    def KNN_W2P(self, quality):
        dict={}
        project=[]

        data = pd.read_excel('project_dataframe.xlsx', sheet_name=0)
        # 导入需要分类的数据
        Xtf_dict = quality

        # 得到了训练集数据与训练集labels
        u = []
        for i in Xtf_dict.keys():
            u.append(i)
        Xf = data[u]  # 得到了训练集数据
        yf = data['name']  # 得到了训练集的labels
        # print(Xf,'\n')
        # print(yf,'\n')

        # 拿出目标的值
        v = []
        for j in Xtf_dict.values():
            v.append(j)
        v = np.array(v)  # 从list转换成array
        v = v.astype(np.float64).tolist()  # 从转换成浮点型并转换为list
        Xtf = [v]
        # print(Xtf)

        # 进行分类
        knnf = KNeighborsClassifier(n_neighbors=1)
        knnf.fit(Xf, yf)

        resultf = knnf.predict(Xtf)
        # resultf = resultf.tolist()
        # print(resultf)
        project.append(resultf[0])
        dict['project'] = project  # 此处存储KNN结果
        probf = knnf.predict_proba(Xtf)
        print('各类型的分类可能性：', probf,'\n')
        return dict  # dict结果为：{'project'：[‘项目名称’]}


# # 输入训练集
# X = [[1, 2], [15, 16], [19, 18], [3, 4], [24, 25], [23, 28]]
# y = [1, 2, 3, 4, 5, 6]
# knn = KNeighborsClassifier(n_neighbors=1) # n_neighbors是与测试数据最接近的样本的数量，默认度量标准为minkowski，p = 2等效于标准欧几里德度量标准
# # 训练样本集
# knn.fit(X, y)
# # 输入测试集
# Xt = [[1.5, 1.7], [11, 14]]
# # 得到分类结果
# result = knn.predict(Xt)
# print(result)  # 得到结果[1]
# result_ture = [1, 1]  # 给出真实值
# # 分类准确度
# score = knn.score(Xt, result_ture)
# print('分类准确度为：',score)
# # 分类对各lable的概率
# prob = knn.predict_proba(Xt)
# print('各lable的概率为：',prob)
# distances, indices = knn.kneighbors(X,n_neighbors=1) # ??
# print('距离为：',distances)
# print(indices)
#
# #
#
# # 用dataframe形式
# data = pd.read_excel('test_dataframe.xlsx', sheet_name=0)
# Xf = data[['COD', 'Q']]
# yf = data['process']
# knnf = KNeighborsClassifier(n_neighbors=1)
# knnf.fit(Xf, yf)
# Xtf = [[50, 3000]]
# resultf = knnf.predict(Xtf)
# print(resultf)
# resultf_ture = ['原水-UF-RO']  # 给出真实值
# scoref = knnf.score(Xtf, resultf_ture)
# print('分类准确度为：',scoref)
# probf = knnf.predict_proba(Xtf)
# print('各lable的概率为：',probf)
#
# # distancesf, indicesf = knnf.kneighbors(Xtf,n_neighbors=1) # ??
# # print('距离为：',distancesf)
# # print(indicesf)
