# coding=utf-8
import os
import re
from pyltp import Segmentor
from htmlconvert2text import convert2txt


# from anago.utils import  load_data_and_labels

class tokenization_entis():
    def __init__(self):
        self.LTP_DATA_DIR = "/home/mm/Downloads/ltp_data_v3.4.0/"
        self.cws_model_path = os.path.join(self.LTP_DATA_DIR, 'cws.model')

        self.segmentor = Segmentor()  # 初始化实例
        self.segmentor.load(self.cws_model_path)  # 加载模型
        self.train_res = self.read_train_res()  # 读取tag文本,防止里面有空格去掉空格
        # self.all_co_names = self.FDDC_co_list()

    def read_train_res(self):
        with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
            train_res = rf.read()
            train_res = re.sub(r'\(', '（', train_res)
            train_res = re.sub(r'\)', '）', train_res)
        return train_res
    def ltp_segmentor_release(self):
        self.segmentor.release()
    def tokenize_enti(self, path11):
        texx, entity_string = convert2txt(path11)
        # sentences = re.split(r'。', texx)
        # sentences.sort(key=len, reverse=True)
        entities = list(set(re.split(r'[\s~、，；/]', entity_string)))
        entities.sort(key=len)
        entities_arrows_list = list(set([x if '~' in x else '' for x in re.split(r'\s', entity_string)]))
        entities_arrows_list.sort(key=len, reverse=True)
        entities_arrows_list = entities_arrows_list[:-1]
        # 找出结果数据行并且把最后的回车符号去掉
        patt_index = re.findall(r'\d{4,10}', path11)[0]
        res_rows = re.findall(r'(?<=\n){}[^\n]+(?=\n)'.format(patt_index), self.train_res)

        # 以下是整理train——res
        # 遍历结果，发现有简称全称的，把匹配的另一半加进去。
        """主要目的是修正train——res文件，里面有简称或者全称，并不统一，为了让简称全称都出现，
            使用正则提取对应的简称或全称，如果有顿号，把那些字串也分开提取，作为标注的标的，当然是先
            把字符长度小的匹配出来，分词之后也是先把长度长的连起来。没问题的"""
        res_paired = {}  # 临时定义一个res的列表，存储修改后的train res
        for x in range(len(res_rows)):
            res_row = res_rows[x]
            for y in range(6):
                res_paired[str(x) + str(y)] = [re.split(r'\t', res_row)[y]]

        for arrow_str in entities_arrows_list:

            for index, result_row in enumerate(res_rows):

                for indi, res_value in enumerate(re.split(r'\t', result_row)):
                    if indi in [0, 1, 4, 5]:
                        continue
                    res_value_list = res_value.split('、')

                    for res_value_split in res_value_list:
                        if res_value_split in entities and res_value_split in arrow_str:
                            # 找出配对的简称或者全称，添加,如果是股权/估值法/金额直接添加并且continue
                            niki, fullna = re.split(r'~', arrow_str)
                            fullna_first = fullna.split('，')[0]
                            niki_split_list = re.split(r'[/、]', niki)
                            # 对应的全称满足三个条件，长度/逗号  以及含有简称的几个字
                            if res_value_split in niki_split_list \
                                    and len(fullna_first) < 18 \
                                    and re.search(re.sub(r'(?<=[^屄\s])', '\s?', res_value_split), fullna_first):
                                res_paired[str(index) + str(indi)].append(fullna_first)
                            """ 由全称查简称时候要避免 公司/本公司/上市公司/发起人/申请人/,
                                含有这几个字的要剔除  """
                            if res_value_split == fullna_first:
                                # 对应的简称满足几个条件： 包含在全程里面，不长于4个字，不等于
                                for niki_split in niki_split_list:
                                    if re.search(re.sub(r'(?<=[^屄\s])', '\s?', fullna_first), niki_split) \
                                            and not re.search(r'(^公司$|^本公司$|环境$|^上市公司$|人$|资产|标的|交易|对方|发行|对象|股东|对手|单位)',
                                                              re.sub(r'\s', '', niki_split)):
                                        res_paired[str(index) + str(indi)].append(niki_split)

        # 遍历公告的每一句，把每一句送进模型。
        # words_n_words = ''
        # for i in sentences:
        words = self.segmentor.segment(entity_string)
        words = ' '.join(words)
        # 分词要使用更好的策略,更长一些,避免太短的句子,重复循环浪费流程
        # # 下面是把所有目标主体合并在一起, 把55%股权这样的先分出来,
        # for ent in entities:
        #     # 把words中所有是实体的中间去掉空格。使用双层sub
        #     # 正则还是要多注释啊
        #     """ re.sub(r'(?<=\w)(?=\w)'','\s?',ent) 是把实体里面的每个字符中间插入“\s?”
        #     表示匹配任何以此序列出现但中间可能有空格的情况,分词之后join成空格分割的。然后找出words
        #     中出现这个序列的地方，将其换成没空格的"""
        #     if len(ent) > 1:
        #         if not re.search(r'([\d.]+%的?(?:股权|股份|权益))', ent):  # 如果没有股权关键字，直接加上空格匹配pattern
        #             patt_ent = re.sub(r'(?<=\w)(?=\w)', r'\s?', ent)
        #         elif len(ent) > 7: # 如果有股权关键字，且长度比较长，就把前面主体提出来，单独分词
        #             patt_ent = re.sub(r'(?<=\w)(?=\w)',r'\s?', re.sub(r'的?[\d.]+%的?(股权|股份|权益)','', ent))
        #         else:
        #             patt_ent = re.sub(r'(?<=\w)(?=\w)', r'\s?', ent)
        #         # 下面一句把words中所有符合主体列表的项目，可能被分词分开的，重新合并起来，单独成行,在test时使用
        #         words = re.sub(r'{}'.format(patt_ent), '\s' + ent + '\s', words)

        # 然后把空格都换成回车,words竖起来了。
        # words = re.sub(r'\s', '\n', words)
        # words = re.sub(r'\n+', '\n', words)
        """把words中所有是结果键值的，后缀上tab键和结果索引号。否则后缀tab键和字母o
            目的是好的，就是让模型更容易找到目标，模型不需要判断开始和结束，
            但是这样的正则太难了， 我无法将所有合适的实体
            全部抽出来，而导致标注的缺失，那么还是把任务给模型了"""
        # for x in range(len(res_rows)):
        #     for y in range(6):
        #         index = str(x)+str(y)
        #         tags_list = res_paired[index]
        for index, tags_list in res_paired.items():
            # 表中的小表，可能有一个或多个成员，遍历一下,包括顿号分割的那些都可以标出来了，不影响合并好的实体字符串。
            for sub_res in sorted(tags_list, key=len, reverse=True):
                if not index.endswith('0') and len(sub_res) > 1:
                    patt_sub_res = re.sub(r'(?<=[^屄\s])', '\s?', sub_res)
                    if re.search(r'{}'.format(patt_sub_res), words):
                        spliter = re.findall(patt_sub_res, words)[0]
                        words_split_list = re.split(spliter, words)
                        spliter_tagged = re.sub(r'\s', '屄{}'.format(index[1]), spliter)
                        words = spliter_tagged.join(words_split_list)
                        # print(words)

                        # words=re.sub(patt_sub_res, sub_res)
                        # words= re.sub(r'{}(?=\n)'.format(sub_res), '\n{}\t{}\n'.format(sub_res, index), words)
            # train——result标注完了，现在标注o,就是把非数字结尾的行加上tab和o
        words = re.sub(r'\s', '\to\n', words)
        words = re.sub(r'(?<=屄\d)', '\n', words)
        words = re.sub(r'屄', '\t', words)
        return words
        # words_n_words += words
        #
        # # print(words)
        # with open('/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/' + res_paired['00'][0] + '.txt',
        #           'w') as af:
        #     af.write(words)
        #     print(path11.split("/")[-1])
        #     # print(words)
        #     # print("%%%%%%%%%%%%%%%%%%%%%%%%this is {}".format(i))


if __name__ == "__main__":
    path_in = "/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/"
    path_out = '/home/mm/FDDC_datasets_dir/tokenized_datasets_for_anago/chongzu/'
    tnt = tokenization_entis()
    done_list = os.listdir(path_out)
    comming_list = os.listdir(path_in)
    for i in comming_list:
        dest_name = i.split('.')[0] + '.txt'
        if dest_name in done_list:
            continue
        else:
            print("now it comes {}".format(i))
            try:
                tnt.tokenize_enti(path_in + i)
            except Exception as e:
                print("sth going wrong wowo  {}".format(e))
                continue
    tnt.ltp_segmentor_release()
# def tokenit(path):
#     path1 = path
#     tnt = tokenization()
#     for htm in os.listdir(path1):
#         tnt.tokenize_enti(path1+htm)


# # 改成多进程的，方便在阿里云高效运行
# if __name__=="__main__":
#     import multiprocessing as mp
#     process_jobs = []
#     path = "/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/"
#     for i in range(5):
#         p = mp.Process(target=tokenit(path))
#         process_jobs.append(p)
#         p.start()
#         p.join()