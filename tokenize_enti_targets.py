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
        self.train_res = self.read_train_res() # 读取tag文本,防止里面有空格去掉空格
        self.all_co_names = self.FDDC_co_list()

    def read_train_res(self):
        with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
            train_res = rf.read()
        return train_res
    def FDDC_co_list(self):
        all_co_names = []
        with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/FDDC_announcements_company_name_20180531.json','r') as rf:
            for text in re.findall(r'(?<=")[^:{}"m]+(?=")', rf.read()):
                if ',' in text:
                    all_co_names+=re.split(r',',text)
                else:
                    all_co_names.append(text)
        return all_co_names

    def tokenize_enti(self,path11):
        texx, entity_string = convert2txt(path11)
        sentences = re.split(r'。', texx)
        # sentences.sort(key=len, reverse=True)
        entities = list(set(re.split(r'[\s~、，；/]', entity_string)))
        entities.sort(key=len)
        entities_arrows =[ x if '~' in x else '' for x in re.split(r'\s', entity_string)]
        entities_arrows.sort(key=len, reverse=True)

        # 找出结果数据行并且把最后的回车符号去掉
        patt_index = re.findall(r'\d{4,10}', path11)[0]
        res_row = re.findall(r'(?<=\n){}[^\n]+(?=\n)'.format(patt_index), self.train_res)[0]


         # 遍历这个结果项，发现有简称全称的，把匹配的另一半加进去。
        """主要目的是修正官方的train——res文件，里面有简称或者全称，并不统一，为了让简称全称都出现，
            使用正则提取对应的简称或全称，如果有顿号，把那些字串也分开提取，作为标注的标的，当然是先
            把字符长度小的匹配出来，分词之后也是先把长度长的连起来。没问题的"""
        res_paired = [[],[],[],[],[],[]]  # 临时定义一个res的列表，存储修改后的train res

        for indi, res_value in enumerate(re.split('\t', res_row)):
            res_paired[indi] = res_value.split('、')
            if res_value in entities:
                # 找出配对的简称或者全称，添加
                for arrow in entities_arrows:
                    if res_value in arrow:
                        niki, fullna = re.split(r'~', arrow)
                        # 即使split出来对方是空值，也填进去

                        # niki_split = re.split(r'[/、]',niki)
                        fullna_first = fullna.split('，')[0]
                        if '，' in fullna and ('、：' not in fullna_first) and len(fullna_first)<14:
                            # fulna_split_comma = re.split(r'，', fullna)
                        # if '，' not in fullna:
                        #     fulna_split_sep = re.split(r'、', fullna)
                        #     res_paired[indi] += fulna_split_sep

                        # res_paired[indi] += [ x if not re.search(r'(公司|人$|资产|标的|交易|对方|对手|单位)', x)  else '' for x in  niki_split]
                            res_paired[indi].append(fullna_first)
                        """ 由全称查简称时候要避免 公司/本公司/上市公司/发起人/申请人/,
                            含有这几个字的要剔除"""

        # 遍历公告的每一句，把每一句送进模型。
        for i in sentences:
            words = self.segmentor.segment(i)
            words = ' '.join(words)
            words = words+' '+'。'+' '  # 加上句号以及句号后面的空格
            for ent in entities:
                # 把words中所有是实体的中间去掉空格。使用双层sub
                # 正则还是要多注释啊
                """ re.sub(r'(?<=\w)(?=\w)'','\s?',ent) 是把实体里面的每个字符中间插入“\s?”
                表示匹配任何以此序列出现但中间可能有空格的情况,分词之后join成空格分割的。然后找出words
                中出现这个序列的地方，将其换成没空格的"""
                if len(ent) > 1:
                    if not re.search(r'([\d.]+%的?(?:股权|股份|权益))', ent):
                        patt_ent = re.sub(r'(?<=\w)(?=\w)', r'\s?', ent)
                    elif len(ent)>7:
                        patt_ent = re.sub(r'(?<=\w)(?=\w)',r'\s?', re.findall(r'[^奸]+(?=的?[\d.]+%的?(?:股权|股份|权益))', ent)[0])
                    else:
                        patt_ent = re.sub(r'(?<=\w)(?=\w)', r'\s?', ent)
                    # 下面一句把words中所有符合主体列表的项目，可能被分词分开的，重新合并起来，单独成行
                    words = re.sub(r'{}'.format(patt_ent), ent, words)
            # # 然后把空格都换成回车,words竖起来了。
            words = re.sub(r'\s', '\n', words)
            words = re.sub(r'\n+', '\n', words)
            """把words中所有是结果键值的，后缀上tab键和结果索引号。否则后缀tab键和字母o"""

            for indi2,res in enumerate(res_paired):
                # 表中的小表，可能有一个或多个成员，遍历一下,包括顿号分割的那些都可以标出来了，不影响合并好的实体字符串。
                for sub_res in res:
                    if len(sub_res) >1:
                        words= re.sub(r'(?<={})(?=\n)'.format(sub_res), '\t{}'.format(indi2),words)
                # train——result标注完了，现在标注o,就是把非数字结尾的行加上tab和o
            words = re.sub(r'(?<!\t\d)(?=\n)', '\to', words)
            with open('output_test_tokenization.txt', 'a') as af:
                af.write(words)
            # print(words+'####################################')
            # print("%%%%%%%%%%%%%%%%%%%%%%%%this is {}".format(i))



if __name__=="__main__":
    path1 = "/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/15500680.html"
    tnt = tokenization()
    tnt.tokenize_enti(path1)