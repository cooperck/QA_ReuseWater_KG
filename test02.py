import ahocorasick
import os
import json
from py2neo import Graph,Node
import re
b=[]
a = '一个项目的COD小于20mg,且电导大于500us怎么办'
b.append(a)
print(a)
print(b[0])
print(str(b))
if a == b:
    print(1)

    ## 总结
    ## ^ 匹配字符串的开始。
    ## $ 匹配字符串的结尾。
    ## \b 匹配一个单词的边界。
    ## \d 匹配任意数字。
    ## \D 匹配任意非数字字符。
    ## x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
    ## x* 匹配0次或者多次 x 字符。
    ## x+ 匹配1次或者多次 x 字符。
    ## x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
    ## (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
    ## (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search 函数返回对象的 groups() 函数获取它的值。
    ## 正则表达式中的点号通常意味着 “匹配任意单字符”