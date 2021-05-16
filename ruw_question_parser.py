class QuestionParser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''针对不同的问题，分开进行处理，得到查询语句'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询项目的工艺
        if question_type == 'project_unit':
            sql = ["MATCH (m:project)-[r:contains_unit]->(n:unit) where m.name = '{0}' return m.name, r.name, n.name, n.id".format(i) for i in entities]
        # 查询用了那个工艺的项目
        if question_type == 'unit_project':
            sql = ["MATCH (m:project)-[r:contains_unit]->(n:unit) where n.name = '{0}' return m.name, r.name, n.name, n.id".format(i) for i in entities]


        # # 查询疾病的防御措施
        # elif question_type == 'disease_prevent':
        #     sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]
        #
        # # 查询疾病的持续时间
        # elif question_type == 'disease_lasttime':
        #     sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(i) for i in entities]
        #
        # # 查询疾病的治愈概率
        # elif question_type == 'disease_cureprob':
        #     sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(i) for i in entities]
        #
        # # 查询疾病的治疗方式
        # elif question_type == 'disease_cureway':
        #     sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]
        #
        # # 查询疾病的易发人群
        # elif question_type == 'disease_easyget':
        #     sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(i) for i in entities]
        #
        # # 查询疾病的相关介绍
        # elif question_type == 'disease_desc':
        #     sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]
        #
        # # 查询疾病有哪些症状
        # elif question_type == 'disease_symptom':
        #     sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        # # 查询症状会导致哪些疾病
        # elif question_type == 'symptom_disease':
        #     sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        # # 查询疾病的并发症
        # elif question_type == 'disease_acompany':
        #     sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        # # 查询疾病的忌口
        # elif question_type == 'disease_not_food':
        #     sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        # # 查询疾病建议吃的东西
        # elif question_type == 'disease_do_food':
        #     sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        #
        # # 已知忌口查疾病
        # elif question_type == 'food_not_disease':
        #     sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        # # 已知推荐查疾病
        # elif question_type == 'food_do_disease':
        #     sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        #
        # # 查询疾病常用药品－药品别名记得扩充
        # elif question_type == 'disease_drug':
        #     sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        #
        # # 已知药品查询能够治疗的疾病
        # elif question_type == 'drug_disease':
        #     sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #     sql = sql1 + sql2
        # # 查询疾病应该进行的检查
        # elif question_type == 'disease_check':
        #     sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        #
        # # 已知检查查询疾病
        # elif question_type == 'check_disease':
        #     sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return sql

    '''解析主函数'''
    def parser_main(self, res_classify):
        ## res_classify格式{'args': {'紫外杀菌器': ['unit'], '一级二段反渗透': ['unit']}, 'question_types': ['unit_project']}
        ### res_classify格式{'args': {'recovery': '70', 'quantity': '200', 'CI_in': '1500'}, 'question_types': ['wquality_process']}
        args = res_classify['args']
        entity_dict = self.build_entitydict(args) #得到问题中的需求对应的字典，肺气肿吃啥，得到的是args:{disease:肺气肿}，问题中有多个关系的进行多关系分类存储
        question_types = res_classify['question_types'] #得到问题中的问题类型，肺气肿吃啥，得到的是['disease_do_food', 'disease_drug']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'project_unit':
                sql = self.sql_transfer(question_type, entity_dict.get('project')) # 翻译为neo4j查询语句
            elif question_type == 'unit_project':
                sql = self.sql_transfer(question_type, entity_dict.get('unit')) # 翻译为neo4j查询语句
            # elif question_type == 'symptom_disease':
            #    sql = self.sql_transfer(question_type, entity_dict.get('symptom'))


            if sql:
                sql_['sql'] = sql #存储问题中一个信息信息{'question_type':'问题类型','sql':[查询语句]}

                sqls.append(sql_) #存储问题中所有的信息

        return sqls # sqls格式：[{'question_type':XXX,'sql':['查询语句']}]





if __name__ == '__main__':
    handler = QuestionParser()
