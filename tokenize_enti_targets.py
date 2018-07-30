#coding=utf-8
import os
import re
from pyltp import Segmentor
from htmlconvert2text import convert2txt
import  codecs


class tokenization():
    def __init__(self):
        self.LTP_DATA_DIR = "/home/mm/Downloads/ltp_data_v3.4.0/"
        self.cws_model_path = os.path.join(self.LTP_DATA_DIR, 'cws.model')

        self.segmentor = Segmentor()  # 初始化实例
        self.segmentor.load(self.cws_model_path)  # 加载模型
        self.train_res = self.read_train_res() # 读取tag文本,防止里面有空格去掉空格

    def read_train_res(self):
        with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
            train_res = rf.read()
        return train_res

    def tokenize_enti(self,path11):
        texx, entity_string = convert2txt(path11)
        sentences = re.split(r'。', texx)
        sentences.sort(key=len, reverse=True)
        entities = list(set(re.split(r'(\s|->|、|，|；|/)', entity_string)))
        entities.sort(key=len, reverse=True)

        # 找出结果数据行并且把最后的回车符号去掉
        patt_index = re.findall(r'\d{4,10}', path11)[0]
        res_row = re.findall(r'(?<=\n){}[^\n]+(?=\n)'.format(patt_index), self.train_res)[0]
         # 遍历这个结果项，发现有简称全称的，把匹配的另一半加进去。
        """主要目的是修正官方的train——res文件，里面有简称或者全称，并不统一，为了让简称全称都出现，
            使用正则提取对应的简称或全称，如果有顿号，把那些字串也分开提取，作为标注的标的，当然是先
            把字符长度小的匹配出来，分词之后也是先把长度长的连起来。没问题的"""
        res_paired = []  # 临时定义一个res的列表，存储修改后的train res
        res_row_enu = enumerate(re.split('\t', res_row))
        for indi, res_value in res_row_enu:
            print(res_value)
            res_paired.append(res_value.split('、'))
            if res_value in entity_string:
                # 找出配对的简称或者全称，添加
                # paired_enti = re.findall(r'((?<={}->)[^\s]+)'.format(res_value), entity_string)
                paired_enti = re.findall(r'(((?<={}->)[^\s]+)|([^\s]+(?=->{})))'.format(res_value, res_value), entity_string)
                if len(paired_enti) >0 :
                    res_paired[indi].append(re.split(r'[/，、]',paired_enti[0])[0])
                    if '、' in paired_enti:
                        for dun2 in paired_enti[0].split('、'):
                            res_paired[indi].append(dun2)

        # 遍历公告的每一句，把每一句送进模型进行训练。
        for i in sentences:
            words = self.segmentor.segment(i) # words字符串，空格分开。
            words = ' '.join(words)
            for ent in entities:
                # 把words中所有是实体的中间去掉空格。使用双层sub
                # 正则还是要多注释啊
                """ re.sub(r'(?<=\w)(?=\w)'','\s?',ent) 是把实体里面的每个字符中间插入“\s?”
                表示匹配任何以此序列出现但中间可能有空格的情况,分词之后join成空格分割的。然后找出words
                中出现这个序列的地方，将其换成没空格的"""
                if len(ent)>1:
                    patt_ent = re.sub('(?<=\w)(?=\w)', r'\s?', ent)
                    words = re.sub(r'{}'.format(patt_ent),ent,words)
            # 然后把空格都换成回车,words竖起来了。
            words= re.sub(r'\s','\n',words)
            # 把words中所有是结果键值的，后缀上tab键和结果索引号。不是的后缀tab键和字母o
            for indi2,res in enumerate(res_paired) :
                # 表中的小表，可能有一个或多个成员，遍历一下,包括顿号分割的那些都可以标出来了，不影响合并好的实体字符串。
                for sub_res in res:
                    words= re.sub(r'(?<={})(?=\n)'.format(res), '\t{}'.format(indi2),words)

            print(words+'\n\n')
            print("%%%%%%%%%%%%%%%%%%%%%%%%this is {}".format(i))



if __name__=="__main__":
    path1 = "/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/15500680.html"
    tnt = tokenization()
    tnt.tokenize_enti(path1)