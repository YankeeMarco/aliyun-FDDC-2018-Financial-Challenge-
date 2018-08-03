#coding=utf-8

import os
from pyltp import Segmentor
from htmlconvert2text import  convert2txt
from pyltp import NamedEntityRecognizer
from pyltp import Postagger
# from pyltp import SentenceSplitter
LTP_DATA_DIR = "/home/47_7/Downloads/ltp_data_v3.4.0/"
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(ner_model_path)
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`

cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')

source_path="/home/47_7/FDDC_datasets_dir/FDDC_announcements_round2_train_html/"
out_path="/home/47_7/FDDC_datasets_text_dir/chongzu/"
listdir = os.listdir(source_path)
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型

segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型
for i in listdir[0:1]:
    html_text,entity_string = convert2txt(source_path+i)
    words = segmentor.segment(html_text)  # 分词
    postags = postagger.postag(words)  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    indices = [i for i, x in enumerate(list(netags)) if x.endswith("Ni")]

    temp_entity=""
    new_list = []
    """以下是对字符串序列中含有实体名称的部分，重新结合在一起，去掉分词造成的间隔，然后在实体前后加缀一个特殊符号{NER#}"""
    for i,x in enumerate(words):
        if (i in indices) and ((i+1) in indices) and (i-1 not in indices):
            temp_entity=x
        elif (i-1 in indices) and (i+1 in indices ) and (i in indices):
            temp_entity+=x
        elif (i-1 in indices) and (i in indices)  and (i+1 not in indices):
            temp_entity+=x
            new_list.append("NER#B"+temp_entity+"NER#E")
        else:
            new_list.append(x)
    for i in new_list:
        print(i)

    with open("/home/47_7/Documents/aliyun-FDDC-2018-Financial-Challenge-/seg_test_while_totalwords.txt", "w") as wf:
        # wf.write(str(list(words)))
        wf.write("".join(new_list))
segmentor.release()  # 释放模型


