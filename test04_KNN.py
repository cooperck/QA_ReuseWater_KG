import numpy as np
import pandas as pd
from pandas import DataFrame,Series
from sklearn.neighbors import KNeighborsClassifier

 
# # 用dataframe形式
    # # 输入数据格式为{'recovery': '70', 'quantity': '200', 'CI_in': '1500'，……}
    # # 数据关键词有：'quantity'，'recovery'，'COD_in'，'CI_in'，'Hardness_in'，'ss_in'
    # # 要求返回结果为{'project'：[‘项目名称’]}
data = pd.read_excel('project_dataframe.xlsx',sheet_name=0)
#测试时候输入数据按格式手动填入
Xtf_dict = {'recovery': '70', 'quantity': '3000', 'CI_in': '2500', 'ss_in': '20'}

# 得到了训练集数据与训练集labels
u = []
for i in Xtf_dict.keys():
    u.append(i)
Xf = data[u] # 得到了训练集数据
yf = data[['unit','name']] # 得到了训练集的labels
print(Xf)
print(yf)

# 拿出目标的值
v = []
for j in Xtf_dict.values():
    v.append(j)
v = np.array(v) # 从list转换成array
v = v.astype(np.float64).tolist() # 从转换成浮点型并转换为list
Xtf = [v]
print(Xtf)

# 进行分类
knnf = KNeighborsClassifier(n_neighbors=1)
knnf.fit(Xf,yf)

resultf = knnf.predict(Xtf)
# resultf = resultf.tolist()
print(resultf)
answers = '与此要求相似的项目为：{0}\n工艺流程为：{1}'.format(resultf[0][1],resultf[0][0])
print(answers)
# resultf_ture = ['原水池→保安过滤器→一级二段反渗透→反渗透产水池'] #给出真实值
# scoref = knnf.score(Xtf,resultf_ture)
# print(scoref)
probf = knnf.predict_proba(Xtf)
print('各类型的分类可能性：',probf)

# 用数组形式输入训练集
# X = [[1,2],[15,16],[19,18],[3,4],[24,25],[23,28]]
# y = [1,2,2,1,3,3]
# knn = KNeighborsClassifier(n_neighbors=3)
# # 训练样本集
# knn.fit(X,y)
# # 输入测试集
# Xt = [[1.5,1.7],[1.1,2.5]]
# # 得到分类结果
# result = knn.predict(Xt)
# print(result) #得到结果[1]
# result_ture = [1,1] #给出真实值
# # 分类准确度
# score = knn.score(Xt,result_ture)
# print(score)
# # 分类对各lable的概率
# prob = knn.predict_proba(Xt)
# print(prob)