from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", username="neo4j", password="cooperck890303")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):  # sqls格式：[{'question_type':XXX,'sql':['查询语句']}]
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data() # ress=[{'m.name':XXX, 'r.name':XXX, 'n.name':XXX,'n.id':XXX}]具体根据answer_perttify得到
                answers += ress # answers=[{'m.name':XXX, 'r.name':XXX, 'n.name':XXX,'n.id':XXX},{'m.name':XXX, 'r.name':XXX, 'n.name':XXX,'n.id':XXX},……]
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        #  查询项目的工艺
        if question_type == 'project_unit': #answers的结果："MATCH (m:project)-[r:contains_unit]->(n:unit) where m.name = '{0}' return m.name, r.name, n.name,n.id"
            unit = [i['n.name'] for i in answers] #得到了所有此项目包含的unit（乱序）
            project = answers[0]['m.name'] # 这里只列了第一格m的名字，可能是bug
            # 下面开始对unit排序
            process_id = []  # 存储流程id
            for i in answers:
                sql_1 = ["MATCH (a:unit)-[b:water_flow]->(c:unit) where c.id = '{0}' RETURN a.id".format(i['n.id'])]
                #print(sql_1)
                ress_1 = self.g.run(sql_1[0]).data()  # [{'a.id':XXX}]
                if len(ress_1) == 0:
                    break
            #print(i['n.id'])
            process_id.append(i['n.id'])  # 输入第一个单元的id
            # print(process_id)
            a = process_id[0]
            for j in answers:
                sql_2 = ["MATCH (a:unit)-[b:water_flow]->(c:unit) where a.id = '{0}' RETURN c.id".format(a)]
                #print(sql_2)
                ress_2 = self.g.run(sql_2[0]).data()  # [{'c.id':XXX}]
                if len(ress_2) == 0:
                    break
                b = ress_2[0]['c.id']
                process_id.append(b)
                a = b
            #print(process_id)  # 得到按顺序的单元id
            # 下面找出单元id对应的单元名称
            process_name = []
            for k in process_id:
                sql_3 = ["MATCH (a:unit) where a.id = '{0}' RETURN a.name".format(k)]
                ress_3 = self.g.run(sql_3[0]).data()  # [{'a.name':XXX}]
                n = ress_3[0]['a.name']
                process_name.append(n)
            #print(process_name)  # 得到按顺序的单元名

            final_answer = '项目{0}包含的工艺单元有：{1}。\n工艺流程为：{2}'.format(project, '；'.join(unit), '-->'.join(process_name))

        # 查询同时含几个工艺的项目
        if question_type == 'unit_project':
            unit = [j['n.name'] for j in answers]  # 得到需要查询的unit
            project = [i['m.name'] for i in answers]  # 得到了含unit中任意一个单元的所有此项目
            #找到同时含有unit里面所有单元的工程
            project_2 = project
            for i in unit:
               project_1 = []
               for j in project:
                   for k in answers:
                       if k['n.name'] == i and k['m.name'] == j:
                           project_1.append(j) #得到含有某个单元的工程，存储进入一个数组
               # 循环完一遍进行并集操作，存入另外一个数组
               project_2 =list(set(project_2).intersection(set(project_1)))

            final_answer = '包含{0}的项目有：{1}。'.format('；'.join(list(set(unit))[:self.num_limit]),'；'.join(list(set(project_2))[:self.num_limit]))

        # 根据水质查询工艺由于之前已经得到了最匹配的项目名称所以 逻辑与 question_type == 'project_unit'一样
        if question_type == 'wquality_process':
            unit = [i['n.name'] for i in answers]  # 得到了所有此项目包含的unit（乱序）
            project = answers[0]['m.name']  # 这里只列了第一格m的名字，可能是bug
            # 下面开始对unit排序
            process_id = []  # 存储流程id
            for i in answers:
                sql_1 = ["MATCH (a:unit)-[b:water_flow]->(c:unit) where c.id = '{0}' RETURN a.id".format(i['n.id'])]
                # print(sql_1)
                ress_1 = self.g.run(sql_1[0]).data()  # [{'a.id':XXX}]
                if len(ress_1) == 0:
                    break
            process_id.append(i['n.id'])  # 输入第一个单元的id
            a = process_id[0]
            for j in answers:
                sql_2 = ["MATCH (a:unit)-[b:water_flow]->(c:unit) where a.id = '{0}' RETURN c.id".format(a)]
                # print(sql_2)
                ress_2 = self.g.run(sql_2[0]).data()  # [{'c.id':XXX}]
                if len(ress_2) == 0:
                    break
                b = ress_2[0]['c.id']
                process_id.append(b) # 得到按顺序的单元id
                a = b
            ## print(process_id)  # 得到按顺序的单元id
            # 下面找出单元id对应的单元名称
            process_name = []
            for k in process_id:
                sql_3 = ["MATCH (a:unit) where a.id = '{0}' RETURN a.name".format(k)]
                ress_3 = self.g.run(sql_3[0]).data()  # [{'a.name':XXX}]
                n = ress_3[0]['a.name']
                process_name.append(n)
            # print(process_name)  # 得到按顺序的单元名

            final_answer = '与此要求相似的项目为：{0}\n推荐的的工艺单元有：{1}。\n工艺流程为：{2}'.format(project, '；'.join(unit), '-->'.join(process_name))



        #     desc = [i['n.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'symptom_disease':
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_cause':
        #     desc = [i['m.cause'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_prevent':
        #     desc = [i['m.prevent'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_lasttime':
        #     desc = [i['m.cure_lasttime'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_cureway':
        #     desc = [';'.join(i['m.cure_way']) for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_cureprob':
        #     desc = [i['m.cured_prob'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_easyget':
        #     desc = [i['m.easy_get'] for i in answers]
        #     subject = answers[0]['m.name']
        #
        #     final_answer = '{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_desc':
        #     desc = [i['m.desc'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0},熟悉一下：{1}'.format(subject,  '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_acompany':
        #     desc1 = [i['n.name'] for i in answers]
        #     desc2 = [i['m.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     desc = [i for i in desc1 + desc2 if i != subject]
        #     final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_not_food':
        #     desc = [i['n.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_do_food':
        #     do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
        #     recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))
        #
        # elif question_type == 'food_not_disease':
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)
        #
        # elif question_type == 'food_do_disease':
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)
        #
        # elif question_type == 'disease_drug':
        #     desc = [i['n.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'drug_disease':
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'disease_check':
        #     desc = [i['n.name'] for i in answers]
        #     subject = answers[0]['m.name']
        #     final_answer = '{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))
        #
        # elif question_type == 'check_disease':
        #     desc = [i['m.name'] for i in answers]
        #     subject = answers[0]['n.name']
        #     final_answer = '通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))



        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()