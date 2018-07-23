#coding=utf-8
import os, re
from htmlconvert2text import convert2txt

list_keywords = ['关联关系', '承诺', '准确', '完整', '证券交易所', '规定', '锁定', '解锁', '补偿', '义务', '解除', '有权', '风险', '募集资金', '发行价格', '应计入', '评估基准日', '承担', '补充协议', '分红', '相应调整', '计算公式', '遵守', '工作日内', '签署协议日', '交割日', '确保', '有权解除', '出具', '若标的']

trick_precedences = [r'(?<=[。；|])[^。；|]*交易对方为[^。|]*[。；|]']
                     # r'标的[^为是]*[为是](.*)',/
                     # r'(交易标的为([^，]的[^的，][，。； ]?)+)',
                     # r'(?<=[。；|])[^。；|]*以\w+法评估[^。|]*[。；|]',
                     # r'(?<=[。；|])[^。；|]*标的资产为(\w的\w{}[^。|]*[。；|]',
                     # r'(?<=[。；|])[^。；|]*\d+\.\d+万元[^。|]*[。；|]',
                     # r'(?<=[。；|])[^。；|]*\d+\.\d+亿元[^。|]*[。；|]']
def findall_reg():
    for i in os.listdir('/home/html/')[100:2770:50]:
        for l in trick_precedences:

            sss = convert2txt('/home/html/'+i)
            reg_out=re.findall(r'{}[^。|]*[。；|]'.format(l), sss, flags=re.X)
            reg_out_final=[]
            list_false_true = []
            for j in reg_out:
                list_false_true = [True if k in j else False for  k in list_keywords]
                if True not in list_false_true:
                    reg_out_final.append(j)
            print(i)
            for i in reg_out_final:
                print(i)

            print('\n\n')


def catch_trick():
    pattern = re.compile(r'([。；|][^。；|，]+标的\w*[为是](?:([^。；|]+(?:股权|股份|控制权|控股权|债权|资产)+))*[。|])', flags=re.X)

    for i in os.listdir('/home/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/'):
        # sss = convert2txt('/home/html/' + i)
        with open("/home/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/"+i,'r') as rf:
            sss = rf.read()
            print("{}       ####################################\n".format(i))
            reg_out = re.findall(pattern, sss)

            if len(reg_out) !=0 :
                for row in reg_out:
                    print(row)


def check_original_sentences():
    with open("/home/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train", 'r') as rf:
        train_res = rf.readlines()
    for i in os.listdir('/home/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/'):
        # sss = convert2txt('/home/html/' + i)

        with open("/home/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/" + i, 'r') as rf:
            # tag = [k.split('\t') if k.startswith(i) else None for k in train_res]
            for rows in train_res:
                if rows.startswith(i.split(".")[0]):
                    trader = rows.split("\t")[2]
            # pattern = re.compile(r'(?<=[。；|/])[^。；|]*(?:{})[^。；|]*(?:股权|股份|控制权|控股权|债权|资产)+[^。|]*[。；|]'.format(trader.replace("、","|")), flags=re.X)
            pattern = re.compile(r'[0-9,，. ]+[亿万]元', flags=re.X)
            sss = rf.read()
            print("{}       ##########{}##########################\n".format(i,trader))
            reg_out = re.findall(pattern, sss)

            if len(reg_out) != 0:
                for row in reg_out:
                    print(row.replace('\n\n','\n')+'\n')




if __name__=='__main__':
    # catch_trick()
    check_original_sentences()