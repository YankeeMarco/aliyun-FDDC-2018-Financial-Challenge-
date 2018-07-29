#coding=utf-8
import os
import re
from pyltp import Segmentor
from htmlconvert2text import convert2txt

class tokenization():
    def __init__(self):
        self.LTP_DATA_DIR = "/home/mm/Downloads/ltp_data_v3.4.0/"
        self.cws_model_path = os.path.join(self.LTP_DATA_DIR, 'cws.model')

        self.segmentor = Segmentor()  # 初始化实例
        self.segmentor.load(self.cws_model_path)  # 加载模型
        self.train_res = re.sub(r'\s','',self.read_train_res()) # 读取tag文本,防止里面有空格去掉空格

    def read_train_res(self):
        with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
            train_res = rf.read()
        return train_res

    def tokenize_enti(self,path11):
        with open(path11, 'r') as rf:
            texx, entity_string = convert2txt(rf.read())
        sentences = re.split(r'。', texx)
        sentences.sort(key=len, reverse=True)
        entities = list(set(re.split(r'(\s|->)', entity_string)))
        entities.sort(key=len, reverse=True)

        # 找出结果数据行并且把最后的回车符号去掉
        res_row = re.search(r'{}[^\n。]+\n'.format(re.findall(r'\d{4,10}', path1)), self.train_res).group()[:-1]
        # 遍历这个结果项，发现有简称全称的，把匹配的另一半加进去。
        res_paired = []  # 临时定义一个res的列表，存储修改后的train res
        for indi, res_value in enumerate(res_row.split('\t')) :
            res_paired.append([res_value])
            if res_value in entity_string:
                if '、' in res_value:
                    for dun1 in res_value.split('、'):
                        res_paired[indi].append(dun1)
                # 找出配对的简称或者全称，添加
                paired_enti = re.findall(r'(((?<={}->)[^\s]+)|([^\s]+(?=->{})))'.format('a', 'a'), entity_string)
                if len(paired_enti) >0 :
                    res_paired[indi].append(paired_enti[0])
                    if '、' in paired_enti:
                        for dun2 in paired_enti[0].split('、'):
                            res_paired[indi].append(dun2)
        # 遍历公告的每一句，把每一句送进模型进行训练。
        for i in sentences:
            words = self.segmentor.segment(i) # words是字符串，空格分开的。
            for ent in entities:
                # 把words中所有是实体的中间去掉空格。使用双层sub
                re.sub(r'{}'.format(re.sub(r'(?<=\w)','\s?',ent)),ent,words)
                # 然后把空格都换成回车,words竖起来了。
                re.sub(r'\s','\n',words)
            # 把words中所有是结果键值的，后缀上tab键和结果索引号。不是的后缀tab键和字母o
            for indi2,res in enumerate(res_paired) :
                # 表中的小表，可能有一个或多个成员，遍历一下,包括顿号分割的那些都可以标出来了，不影响合并好的实体字符串。
                for sub_res in res:
                    re.sub(r'(?<={})(?=\n)'.format(res), '\t{}'.format(indi2),words)

            print(words+'\n\n')
            print("%%%%%%%%%%%%%%%%%%%%%%%%this is {}".format(i))



if __name__=="__main__":
    path1 = "/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/15500680.html"
    tnt = tokenization()
    tnt.tokenize_enti(path1)