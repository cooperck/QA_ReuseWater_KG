import re

# question = input('input an question:')
# print(question)
# print(re.findall(question ,"回收率"))

q = '回收率70%，流量70吨每天，电导率1500us，用什么工艺'
data = {'args': {'回收率': ['recovery'], '流量': ['quantity'], '电导率': ['CI_in']}, 'question_types': ['wquality_process']}
a = data['args']
for i in a.keys():
    pattern = "({0})(\d+)".format(i)
    input_str = q
    match = re.findall(pattern, input_str)
    number = match[0][1]
    print(number)
    b=a[i]
    print(b)
    a[i]=number
    a[b[0]] = a.pop(i)
print(a)
data['args']=a
print(data)



# pattern = "(回收率)(\d+)"
#
# input_str = "回收率70%，流量200吨每天，电导率1500us，用什么工艺"
#
# match = re.findall(pattern, input_str)
# match1 =match[0][1]
# print(match1)