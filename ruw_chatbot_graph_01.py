from ruw_question_classifier_01 import *
from ruw_question_parser_01 import *
from ruw_answer_search_01 import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionParser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '没能理解您的问题，我数据量有限。。。能不能问的标准点'
        res_classify = self.classifier.classify(sent)  #从输入的问题通过QuestionClassifier先得到classify
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify) #用classify结果通过QuestionParser得到sql
        final_answers = self.searcher.search_main(res_sql) #用sql结果通过AnswerSearcher得到final_answers
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('咨询:')
        answer = handler.chat_main(question)
        print('客服机器人:', answer)

