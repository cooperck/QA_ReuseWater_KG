#-*- coding : utf-8 -*-
# coding: utf-8


import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.project_path = os.path.join(cur_dir, 'dict/project.txt')
        self.unit_path = os.path.join(cur_dir, 'dict/unit.txt')
        self.deny_path = os.path.join(cur_dir, 'dict/deny.txt')

        # 加载特征词
        self.project_wds= [i.strip() for i in open(self.project_path) if i.strip()]#encoding="utf-8"
        self.unit_wds= [i.strip() for i in open(self.unit_path) if i.strip()]

        self.region_words = set(self.project_wds + self.unit_wds)
        # deny是一个反义词的合集，单独由人工列出
        self.deny_words = [i.strip() for i in open(self.deny_path,encoding="utf-8") if i.strip()]
        # 构造领域actree，ac多模式匹配算法里的方法
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建关键词与对应类型的词典
        self.wdtype_dict = self.build_wdtype_dict() #格式为[{'项目或单元名'：'project或unit'},{'项目或单元名'：'project或unit'},{数：'quantity'}……]



        # 工艺参数单位词，人工列出
        self.Qunit_qwds = ['吨/天', '吨每天', 'CMD', 't/d', 'tph', 't/h', 'm3/h', '吨每小时']
        self.Recovunit_qwds = ['%']
        self.CODunit_qwds = ['mg', 'mg/L', 'mg/l', 'ppm']
        self.CIunit_qwds = ['Us', 'us', 'us/cm', 'ms', 'Ms', 'ms/cm']
        self.Hardunit_qwds = ['mg', 'mg/L', 'mg/l', 'ppm']
        self.SSunit_qwds = ['mg', 'mg/L', 'mg/l', 'ppm']




        # 问句疑问词，人工列出
        self.process_qwds = ['哪些工艺单元','工艺单元有哪些','什么工艺', '什么流程', '什么工艺流程','哪些工艺','工艺有哪些', '哪些流程', '哪些工艺流程','哪种工艺', '哪种流程', '哪种工艺流程','工艺是什么','工艺流程是什么']
        self.project_qwds = ['什么项目', '什么工程', '哪个项目', '哪个工程','项目有哪些','有哪些项目']
        self.unit_qwds = ['什么设备', '什么单元', '哪个设备', '哪个单元']






        print('model init finished ......') #以上是输入问答模型的基础数据

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        project_dict = self.check_project(question) #check_project：用wdtype_dict进行问句过滤，最终构建成一个符合问句的关键词和关键词类型的字典
        if not project_dict:
            return {}
        data['args'] = project_dict # 将关键词和关键词类型的字典输入一个更大的字典data，这里面存储了问题中提到了哪些节点
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in project_dict.values(): # 将关键词类型的存储为type
            types += type_
        question_type = 'others'

        question_types = []

        ## 目标解决以下问题
        # 1 知道项目名称查工艺
        # 2 知道某个工艺查哪个项目用了这个工艺
        # 3 知道进出水的水量、水质、回收率的一个或几个参数查工艺
        # 4 知道某个单元的进水或出水工艺参数名称查项目名称
        # 5 查询某个单元的最高、最低、平均进水或出水工艺参数（附加）
        # 6 知道工艺参数的范围或不与数据库完全匹配的值，进行工艺流程模糊匹配（目标）

        # 1 知道项目名称查工艺
        # 如果问句中包含流程查询且明确的项目名称在查询语句中，如：
        # 蒙西污水处理厂的工艺是什么……日铭三期回用水用了哪些工艺……泰州可利放流回用水包含哪些工艺
        if self.check_words(self.process_qwds, question) and ('project' in types):
            question_type = 'project_unit'
            question_types.append(question_type)

        # 2 知道某个工艺查哪个项目用了这个工艺
        # 如果问句中包含项目查询且明确的某个单元名称在查询语句中，如：
        # 用了一级二段反渗透的项目有哪些……用自清洗过滤器的有哪些项目……什么项目用了浸没式超滤
        if self.check_words(self.project_qwds, question) and ('unit' in types):
            question_type = 'unit_project'
            question_types.append(question_type)

        # # 6 知道工艺参数的范围或不与数据库完全匹配的值，进行工艺流程模糊匹配（目标）
        # if self.check_words(self.project_qwds, question) and ('unit' in types):
        #     question_type = 'wquality_process'
        #     question_types.append(question_type)
        #

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types


        return data

    '''筛选出构造词对应的类型,也就是够造'args'后面的内容'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.project_wds:
                wd_dict[wd].append('project')
            if wd in self.unit_wds:
                wd_dict[wd].append('unit')

        return wd_dict
        #wd_dict格式为[{'项目或单元名'：'project或unit'},{'项目或单元名'：'project或unit'},{数：'quantity'}……]
        ## 格式或为{}

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤从wdtype_dict中过滤出符合question的关键词和关键词类型的字典'''
    def check_project(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)