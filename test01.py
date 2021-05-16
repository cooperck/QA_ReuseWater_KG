import ahocorasick
import os
import json
from py2neo import Graph,Node
import pandas as pd

a = [['assdds','dad'],['111','dasd'],['1223','23213']]
b = ['assdds','111','dad']
c = ['assdds','121','g4d']
d = {"a":['assdds','dad'],"b":['111','dasd'],"c":['1223','23213']}
e = [{"a":'assdds',"b":['111','dasd'],"c":['1223','23213']},{"a":'bb',"b":['bb1','dasd'],"c":['1b3','23213']},{"a":'accs',"b":['c11','dasd'],"c":['1c23','23213']}]
f = {"a":['dsa'],"b":['dsdd'],"c":['dsfd']}
x ={}
y=[]
# project_2 =pd.DataFrame.from_dict(f)
# print(project_2)
dicts = [{"ds": "SC_CsD", "dds": "SC_fD", "ddss": "SC_CgD"}, {"ds": "SC_2", "dds": "SC3_2", "ddss": "SC5_2"}]
p_i={}
key1=[]
for dict in dicts:
    # print(dict)
    # print(list(dict.keys()))
    for key in list(dict.keys()):
        key1.append(key)
    # print(key1)
    for k in key1:
        p_i[k]=[]
    for k in key1:
        # print(p_i[k])
        # print(dict[k])
        p_i[k].append(dict[k])
    pi=pd.DataFrame.from_dict(p_i)
    print(pi)

# for i in dicts.values():
#     print(i)
# for i in dicts.keys():
#     print(dicts[i])
    # print(dict.values("10.162"))