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



def catch_trick2():
    pattern = re.compile(r'(?<=(\.\d))\d{0,6}(\s{0,3}万元)', flags=re.X)

    for i in os.listdir('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/'):
        # sss = convert2txt('/home/html/' + i)
        with open("/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/"+i,'r') as rf:
            sss = rf.read()
            print("{}       ####################################\n".format(i))
            reg_out = re.findall(pattern, sss)

            if len(reg_out) !=0 :
                for row in reg_out:
                    for i in row:
                        print(i)
def catch_trick3():
    pattern = re.compile(r'美元', flags=re.X)

    for i in os.listdir('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/'):
        # sss = convert2txt('/home/html/' + i)
        with open("/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/"+i,'r') as rf:
            sss = rf.read()
            print("{}       ####################################\n".format(i))
            reg_out = re.findall(pattern, sss)

            if len(reg_out) !=0 :
                for row in reg_out:
                    for i in row:
                        print(i)

def catch_trick4():
    pattern = re.compile(r'((?:[^\d.,;()]{3,8}指[^\d.,;()]{8,18}\n+)(?:[^\d.,;()]{3,8}指[^\d.,;()]{8,18}\n+)(?:[^\d.,;()]{3,8}指[^\d.,;()]{8,18}\n+))', flags=re.X)

    for i in os.listdir('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/'):
        # sss = convert2txt('/home/html/' + i)
        with open("/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/"+i,'r') as rf:
            sss = rf.read()
        print("{}       ####################################\n".format(i))
        reg_out = re.findall(pattern, sss)

        if len(reg_out) !=0 :
            for row in reg_out:
                print(str(row))




def catch_trick5():

    with open('entity_string_test.txt','a') as af:

        for i in os.listdir('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/')[0:2770:10]:
            # sss = convert2txt('/home/html/' + i)
            with open("/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/"+i,'r') as rf:
                sss = rf.read()
            print("{}       ####################################\n".format(i))
            sss = re.sub(r'[\s\n]', '', sss)  # 把所有空格回车去掉，表格的变动信息不要了，此任务不需要

            reg_out = re.findall(r'<td>[^<>]+</td><td>指</td><td>[^<>]+</td>',sss)

            if len(reg_out) !=0 :
                for i in reg_out:
                    first = i.split("</td><td>")[0][4:]
                    third = i.split("</td><td>")[2][:-5]
                    if '公司' in i:
                        # print(first+'-->'+third)
                        af.write(first+'-->'+third+'\n')

def catch_trick6():


    for i in os.listdir('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/'):
        # sss = convert2txt('/home/html/' + i)
        with open("/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/"+i,'r') as rf:
            sss = rf.read()

        sss = re.sub(r'[\s\n]', '', sss)  # 把所有空格回车去掉，表格的变动信息不要了，此任务不需要
        sss = re.sub(r'<[^<>]>','',sss)
        reg_out = re.findall(r'(?<!\d)[\d,，%.]+[万千]?股[^股，。；\s\n]{0，10}(股份|股)',sss)

        if len(reg_out) !=0 :
            print("{}       ####################################\n".format(i))
            for row in reg_out:
                print(str(row))

def catch_trick7():

    for i in os.listdir('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/'):
        # sss = convert2txt('/home/html/' + i)
        with open("/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/"+i,'r') as rf:
            sss = rf.read()

        sss = re.sub(r'[\s\n]', '', sss)  # 把所有空格回车去掉，表格的变动信息不要了，此任务不需要
        sss = re.sub(r'<[^<>]>','',sss)
        reg_out = re.findall(r'([\d.]+%的?(?:股权|股份|权益))',sss)

        if len(reg_out) !=0 :
            print("{}       ####################################\n".format(i))
            for row in reg_out:
                print(str(row))

def catch_trick8():
    from htmlconvert2text import convert2txt
    def read_train_res():
        with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
            train_res = rf.read()
        return train_res
    train_re = read_train_res()

    for i in os.listdir('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/')[0:2000:20]:
        # sss = convert2txt('/home/html/' + i)
        sss,_ = convert2txt("/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/"+i)


        row_train_re = re.search(r'{}[^\n。]+\n'.format(i.split(".")[0]),train_re).group()[:-1]
        print("###########################################################{}".format(i))
        for index, res_enti in enumerate(row_train_re.split('\t')) :

            if len(res_enti)>1:
                print("@@@this is the {}th key_value{}".format(index,res_enti))
                res_find = re.findall(r'{}'.format(res_enti), sss)

                if len(res_find)>0:
                    print(res_find)
                else:
                    print("@@@")

def catch_trick88():
    from htmlconvert2text import convert2txt
    def read_train_res():
        with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
            train_res = rf.read()
        return train_res

    train_re = read_train_res()

    for i in os.listdir('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/')[
             0:2000:20]:
        # sss = convert2txt('/home/html/' + i)
        sss, ent_str = convert2txt("/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/" + i)

        row_train_re = re.search(r'{}[^\n。]+\n'.format(i.split(".")[0]), train_re).group()[:-1]
        print("###########################################################{}".format(i))
        for index, res_enti in enumerate(row_train_re.split('\t')):

            if len(res_enti) > 1:
                print("@@@this is the {}th key_value{}".format(index, res_enti))
                res_find = re.findall(r'{}'.format(res_enti), ent_str)

                if len(res_find) > 0:
                    print(res_find)
                else:
                    print("@@@")

def catch_trick888():
    from htmlconvert2text import convert2txt
    # def read_train_res():
    #     with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
    #         train_res = rf.read()
    #     return train_res
    #
    # train_re = read_train_res()

    for i in os.listdir('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/')[
             0:2688:18]:
        # sss = convert2txt('/home/html/' + i)
        sss, ent_str = convert2txt("/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/" + i)
        if len(ent_str) > 10:
            with open('checkregexentity.txt' , 'a') as af:
                af.write(ent_str + "\n")
            print("OOOOOOOOOOO")
        else:
            print(i)
        # row_train_re = re.search(r'{}[^\n。]+\n'.format(i.split(".")[0]), train_re).group()[:-1]
        # print("###########################################################{}".format(i))
        # for index, res_enti in enumerate(row_train_re.split('\t')):
        #
        #     if len(res_enti) > 1:
        #         print("@@@this is the {}th key_value{}".format(index, res_enti))
        #         res_find = re.findall(r'{}'.format(res_enti), ent_str)
        #
        #         if len(res_find) > 0:
        #             print(res_find)
        #         else:
        #             print("@@@")

if __name__=='__main__':
    catch_trick888()
    # check_original_sentences()