from py2neo import Graph

g = Graph("http://localhost:7474", username="neo4j", password="cooperck890303")
num_limit = 20


print(1)
queries = ["MATCH (m:project)-[r:contains_unit]->(n:unit) where m.id = '{0}'  RETURN m.name, r.name, n.name, n.id".format('DX-01')]
print(queries)
answers = []
ress = g.run(queries[0]).data()
print(ress)
answers += ress
print(answers)
# unit_id = answers[0]['n.id']
# print('unit_id',unit_id)
process_id=[] # 存储流程id
for i in answers:
    sql_1 = ["MATCH (a:unit)-[b:water_flow]->(c:unit) where c.id = '{0}' RETURN a.id".format(i['n.id'])]
    print(sql_1)
    ress_1 = g.run(sql_1[0]).data() # [{'a.id':XXX}]
    if len(ress_1) == 0:
       break
#print(i['n.id'])
process_id.append(i['n.id'])#输入第一个单元的id
#print(process_id)
a = process_id[0]
for j in answers:
    sql_2 = ["MATCH (a:unit)-[b:water_flow]->(c:unit) where a.id = '{0}' RETURN c.id".format(a)]
    print(sql_2)
    ress_2 = g.run(sql_2[0]).data()#[{'c.id':XXX}]
    if len(ress_2) ==0:
        break
    b=ress_2[0]['c.id']
    process_id.append(b)
    a=b
print(process_id) #得到按顺序的单元id
# 下面找出单元id对应的单元名称
process_name=[]
for k in process_id:
    sql_3 = ["MATCH (a:unit) where a.id = '{0}' RETURN a.name".format(k)]
    ress_3 = g.run(sql_3[0]).data()  # [{'a.name':XXX}]
    n=ress_3[0]['a.name']
    process_name.append(n)
print(process_name)
x='工艺流程为：{0}'.format('-->'.join(list(set(process_name))))
print(x)