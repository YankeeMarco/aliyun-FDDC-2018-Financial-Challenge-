import os
from pyltp import Segmentor
from htmlconvert2text import  convert2txt
from pyltp import NamedEntityRecognizer
from pyltp import Postagger
# from pyltp import SentenceSplitter
# sents = SentenceSplitter.split('元芳你怎么看？我就趴窗口上看呗！')
LTP_DATA_DIR = "/home/mm/Downloads/ltp_data_v3.4.0/"
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(ner_model_path)
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`

cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')

source_path="/home/mm/Downloads/round1_train_20180518/dingzeng/html/"
out_path="/home/mm/aliyunChallenge/"
listdir = os.listdir(source_path)
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型

segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型
for i in listdir[0:1]:
    html_text = convert2txt(source_path+i)
    words = segmentor.segment(html_text)  # 分词
    postags = postagger.postag(words)  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    indices = [i for i, x in enumerate(list(netags)) if x.endswith("Ni")]

    temp_entity=""
    new_list = []
    for i,x in enumerate(words):
        if (i in indices) and ((i+1) in indices) and (i-1 not in indices):
            temp_entity=x
        elif (i-1 in indices) and (i+1 in indices ) and (i in indices):
            temp_entity+=x
        elif (i-1 in indices) and (i in indices)  and (i+1 not in indices):
            temp_entity+=x
            new_list.append(temp_entity)
        else:
            new_list.append(x)
    print(new_list)

    with open("/home/mm/aliyunChallenge/seg_test_while_totalwords.txt", "w") as wf:
        # wf.write(str(list(words)))
        wf.write("-".join(new_list))
segmentor.release()  # 释放模型


