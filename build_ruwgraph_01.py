#选材自开源项目(刘焕勇，中国科学院软件研究所)，数据集来自互联网爬虫数据
import os
import json
from py2neo import Graph,Node

class MedicalGraph:  #########这里名字后期改,01版本只有项目和单元的关系
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/reusewater_data_01.json')
        self.g = Graph("http://localhost:7474", username="neo4j", password="cooperck890303")

    '''读取文件'''
    def read_nodes(self):
        # 构建节点，共 2 类节点
        projects = []  # 项目
        units = []  # 处理单元
        project_infos = []  # 项目信息

        # 构建节点实体关系
        rels_proj2unit = [] #　项目－单元包含关系
        rels_unit2unit = [] #单元-单元的连接关系



        count = 0
        for data in open(self.data_path):
            project_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            project = data_json['name']
            project_dict['name'] = project
            projects.append(project)   #应该是去除重复元素
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


            if 'recommand_unit' in data_json: #这也是一个节点
                units += data_json['recommand_unit']
                for unit in data_json['recommand_unit']:
                    rels_proj2unit.append([project, unit])


            if 'desc' in data_json: #这是一个disease节点的属性
                project_dict['desc'] = data_json['desc']

            if 'category' in data_json:
                project_dict['category'] = data_json['category']

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

            project_infos.append(project_dict)

        return set(projects), set(units), project_infos,\
               rels_proj2unit

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
            node = Node("project", name=project_dict['name'], desc=project_dict['desc'],
                        category=project_dict['category'] ,quantity=project_dict['quantity'],
                        recovery=project_dict['recovery'],COD_in=project_dict['COD_in'],
                        CI_in=project_dict['CI_in'], Hardness_in=project_dict['Hardness_in'],
                        ss_in=project_dict['ss_in'], COD_out=project_dict['COD_out'],
                        CI_out=project_dict['CI_out'], Hardness_out=project_dict['Hardness_out'],
                        ss_out=project_dict['ss_out'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型unit'''
    def create_graphnodes(self):
        projects, units, project_infos, rels_proj2unit = self.read_nodes()
        self.create_project_nodes(project_infos)
        self.create_node('unit', units)
        print(len(units))
        return


    '''创建实体关联边''' #定义后给下一个create_graphrels用
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name): #rel_type关系类型, rel_name关系名字也是关系的属性
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
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        projects, units, project_infos, rels_proj2unit = self.read_nodes()
        self.create_relationship('project', 'unit', rels_proj2unit, 'contains_unit', '包含的工艺单元')



    '''导出数据'''
    def export_data(self):
        projects, units, project_infos, rels_proj2unit = self.read_nodes()
        f_unit = open('unit.txt', 'w+')
        f_project = open('project.txt', 'w+')

        f_unit.write('\n'.join(list(units)))
        f_project.write('\n'.join(list(projects)))

        f_unit.close()
        f_project.close()


        return



if __name__ == '__main__':
    handler = MedicalGraph()
    handler.export_data()
    handler.create_graphnodes()
    handler.create_graphrels()
