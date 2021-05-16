#选材自开源项目(刘焕勇，中国科学院软件研究所)，数据集来自互联网爬虫数据
import os
import json
from py2neo import Graph,Node
import numpy as np
import pandas as pd
from pandas import DataFrame,Series



class RUWGraph:  #########这里名字后期改,02版本只项目和单元的关系##单元和单元的关系
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/reusewater_data_02.json')
        self.g = Graph("http://localhost:7474", username="neo4j", password="cooperck890303")

    '''读取文件'''
    def read_nodes(self):
        # 构建节点，共 2 类节点
        projects = []  # 项目
        project_infos = []  # 项目信息
        unit_infos = []  # 项目内的单元信息
        rels_unit2unit = []  # 单元-单元的连接关系
        unit_relation_attribute = [] # 单元-单元的连接关系的属性

        # 构建节点实体关系
        rels_proj2unit = [] #　项目－单元包含关系




        count = 0
        #注意以下+=操作对于数组是把数组中每个元素单独加入，append数组是把数组作为整体加入称为一个元素
        for data in open(self.data_path):
            project_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            project = data_json['_id']
            project_dict['_id']=project
            projects.append(project)   #应该是去除重复元素
            project_dict['name'] = ''
            project_dict['desc'] = ''
            project_dict['category'] = ''
            project_dict['quantity'] = ''
            project_dict['COD_in'] = ''
            project_dict['CI_in'] = ''
            project_dict['Hardness_in'] = ''
            project_dict['ss_in'] = ''
            project_dict['COD_out'] = ''
            project_dict['CI_out'] = ''
            project_dict['Hardness_out'] = ''
            project_dict['ss_out'] = ''
            project_dict['unit'] = ''

            unit_infos_1 = []#用于存储每个工程的所有单元属性数组


            if 'recommand_unit' in data_json: #进行这个项目中的单元节点读取,读取单元节点并读取项目-单元关系
                units = [] # 处理单元
                unit_1 = []# 过渡用
                units += data_json['recommand_unit']
                # 把数组形式转化为str，元素之间用→分割
                units_p = "→".join(str(i) for i in units)
                project_dict['unit'] = units_p

                if 'unit_attribute' in data_json:  # 为每个单元增加属性

                    unit_1 += data_json['unit_attribute']
                    unit_dict={}

                    l=len(units)
                    print(count)
                    count_1=0
                    for i in range(0,l):
                        count_1+=1
                        unit_dict = {}
                        unit_dict['name']= units[i]
                        unit_dict['_id']= unit_1[i][0]
                        rels_proj2unit.append([project, unit_dict['_id']])#建立project——unit_id的联系
                        unit_dict['规格1'] = unit_1[i][1]
                        unit_dict['规格2'] = unit_1[i][2]
                        unit_infos_1.append(unit_dict)
                        print(count_1)
                        #至此建立一个工程中的unit节点的所有信息群，一个数组


                if 'unit_relation' in data_json: #读取单元单元关系关系
                    rels_unit2unit_1=[]#临时使用

                    rels_unit2unit_1 += data_json['unit_relation']
                    if 'unit_relation_attribute' in data_json:  # 为每个单元单元关系关系增加属性
                        l1=len(rels_unit2unit_1)
                        l2=len(units)
                        x=0
                        y=0
                        for i in range(0,l1):
                            n1 = rels_unit2unit_1[i][0] #取出单元单元关系中的第一个单元名
                            n2 = rels_unit2unit_1[i][1] #取出单元单元关系中的第二个单元名
                            #把对应单元的id找出来
                            for j in range(0,l2):
                                if units[j]== n1:
                                    x=j
                                if units[j] == n2:
                                    y=j

                            id_1=unit_1[x][0]#单元单元关系中的第一个单元id
                            id_2=unit_1[y][0]  # 单元单元关系中的第二个单元id
                            rels_unit2unit.append([id_1, id_2]) # 建立所有基于单元id的联系数组，不对工程划分

                     # 为每个单元单元联系增加属性
                        attri_unit2unit_1 = []  # 临时使用,每读取一条数据就重新归零一次
                        attri_unit2unit_1 += data_json['unit_relation_attribute'] #把每次条数据中的关系属性输入到临时列表中
                        unit_relation_attribute += attri_unit2unit_1 #把每次的临时列表关系属性输入到永久列表中，不对工程划分

            if 'name' in data_json:  # 这是一个disease节点的属性
                project_dict['name'] = data_json['name']

            if 'desc' in data_json:
                project_dict['desc'] = data_json['desc']

            if 'category' in data_json:
                # 把数组形式转化为str，元素之间用|分割
                category_p="|".join(str(i) for i in data_json['category'])
                project_dict['category'] = category_p

            if 'quantity' in data_json:
                project_dict['quantity'] = data_json['quantity']

            if 'recovery' in data_json:
                project_dict['recovery'] = data_json['recovery']

            if 'COD_in' in data_json:
                project_dict['COD_in'] = data_json['COD_in']

            if 'CI_in' in data_json:
                project_dict['CI_in'] = data_json['CI_in']

            if 'Hardness_in' in data_json:
                project_dict['Hardness_in'] = data_json['Hardness_in']

            if 'ss_in' in data_json:
                project_dict['ss_in'] = data_json['ss_in']

            if 'COD_out' in data_json:
                project_dict['COD_out'] = data_json['COD_out']

            if 'CI_out' in data_json:
                project_dict['CI_out'] = data_json['CI_out']

            if 'Hardness_out' in data_json:
                project_dict['Hardness_out'] = data_json['Hardness_out']

            if 'ss_out' in data_json:
                project_dict['ss_out'] = data_json['ss_out']

            project_infos.append(project_dict) #把每个项目的基本信息字典组成一个大的数组，大数组中每一个单元对应一个工程
            unit_infos.append(unit_infos_1) #把每个项目的单元信息数组组成一个大的数组，大数组中每一个单元对应一个工程

        return set(projects),  project_infos, unit_infos, rels_proj2unit, rels_unit2unit, unit_relation_attribute
    # 返回值为：
    # set(projects)：各工程的id
    # project_infos：一个数组，[数组]中每个元素为某一个工程的基础信息{字典}，如project_infos[0]得到第一个工程的基础数据字典
    # unit_infos：一个数组，[数组]中每个元素为某一个工程的包含的所有单元的信息[数组]，这个数组由代表各工艺单元信息的{字典}组成，如unit_infos[0][1]代表，第一个工程中第二个单元的基础数据字典，包括name，id，规格1，规格2
    # rels_proj2unit：一个数组，[数组]中每个元素为工程id与单元id组成的[数组]
    # rels_unit2unit：一个数组，[数组]中每个元素为基于两个单元id的联系[数组]
    # unit_relation_attribute：一个数组，[数组]中每个元素为某个单元单元联系的属性[数组]，他的顺序与rels_unit2unit一致，属性[数组]中的每个数代表了各工艺参数

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心项目的节点'''
    def create_project_nodes(self, project_infos):
        count = 0
        for project_dict in project_infos:
            node = Node("project", id=project_dict['_id'],name=project_dict['name'], desc=project_dict['desc'],
                        category=project_dict['category'] ,quantity=project_dict['quantity'],
                        recovery=project_dict['recovery'],COD_in=project_dict['COD_in'],
                        CI_in=project_dict['CI_in'], Hardness_in=project_dict['Hardness_in'],
                        ss_in=project_dict['ss_in'], COD_out=project_dict['COD_out'],
                        CI_out=project_dict['CI_out'], Hardness_out=project_dict['Hardness_out'],
                        ss_out=project_dict['ss_out'],recomand_unit=project_dict['unit'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱工艺单元的节点'''
    def create_unit_nodes(self, unit_infos):
        count = 0
        for unit_p in unit_infos:
            for unit_dict in unit_p:
                node = Node("unit", name=unit_dict['name'], id=unit_dict['_id'],
                            attribute_1=unit_dict['规格1'] ,attribute_2=unit_dict['规格2'])
                self.g.create(node)
                count += 1
                print(count)
        return

    '''创建知识图谱实体节点类型'''
    def create_graphnodes(self):
        projects,  project_infos, unit_infos, rels_proj2unit, rels_unit2unit, unit_relation_attribute = self.read_nodes()
        self.create_project_nodes(project_infos)
        self.create_unit_nodes(unit_infos)
        print(len(unit_infos))
        return

    '''创建project到unit之间的实体关联边'''  # 定义后给下一个create_graphrels用
    def create_relationship_pro2unit(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.id='%s'and q.id='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return


    '''创建unit之间的实体关联边''' #定义后给下一个create_graphrels用
    def create_relationship_unit(self, start_node, end_node, edges, rel_type, rel_attr): #rel_type关系类型, rel_name关系名字也是关系的属性
        count = 0
        # 去重处理
        set_edges = []
        set_attrs = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))


        for i in range(0,all):
            edge = set_edges[i].split('###')
            attr = rel_attr[i]
            p = edge[0]
            q = edge[1]
            #提取每个水流的各指标
            print(attr[0])
            a_1 = attr[0]
            a_2 = attr[1]
            a_3 = attr[2]
            a_4 = attr[3]
            a_5 = attr[4]
            query = "match(p:%s),(q:%s) where p.id='%s'and q.id='%s' create (p)-[rel:%s{Q:'%s',COD:'%s',Ci:'%s',Hard:'%s',SS:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, a_1, a_2, a_3, a_4, a_5) # 注意id在写入时候要有_,查询不需要下划线
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        projects, project_infos, unit_infos, rels_proj2unit, rels_unit2unit, unit_relation_attribute = self.read_nodes()
        # 创建project-unit的关系
        self.create_relationship_pro2unit('project', 'unit', rels_proj2unit, 'contains_unit', '包含的工艺单元')
        #创建unit-unit的关系
        self.create_relationship_unit('unit', 'unit', rels_unit2unit, 'water_flow',unit_relation_attribute)



    '''导出数据'''
    def export_data(self):
        projects,  project_infos, unit_infos, rels_proj2unit, rels_unit2unit, unit_relation_attribute = self.read_nodes()
        # 导出节点名
        f_unit = open('unit.txt', 'w+')
        f_project = open('project.txt', 'w+')
        l_1=len(unit_infos)
        print(l_1)
        for i in range(0,l_1):
            l_2 = len(unit_infos[i])
            for j in range(0,l_2):
                f_unit.write(unit_infos[i][j]['name'])
                if j != l_2 - 1:
                    f_unit.write('\n')
        l_3=len(project_infos)
        for m in range(0,l_3):
            f_project.write(project_infos[m]['name'])
            if m != l_3 - 1:
                f_project.write('\n')
        f_unit.close()
        f_project.close()

        # 导出各project的dataframe用于分类器
        p_i = {}
        for dict1 in project_infos:
            key_11 = []
            for key_1 in list(dict1.keys()):
                key_11.append(key_1)
            for k1 in key_11:
                p_i[k1] = []
        for dict in project_infos:
            key1=[]
            for key in list(dict.keys()):
                key1.append(key)
            for k in key1:
                p_i[k].append(dict[k])
            print('存储project数据:'+str(len(p_i)))
        pi = pd.DataFrame.from_dict(p_i)
        pi.to_excel('project_dataframe.xlsx')

        return



if __name__ == '__main__':
    handler = RUWGraph()
    # 输出节点的名字：
    handler.export_data()
    handler.create_graphnodes()
    handler.create_graphrels()
