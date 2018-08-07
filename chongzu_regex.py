import re, os
from htmlconvert2text import convert2txt
import  collections
import random
from pyltp import Segmentor
import pickle

def read_train_res():
    with open('/home/mm/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
        train_res = rf.read()
        train_res = re.sub(r'\(', '（', train_res)
        train_res = re.sub(r'\)', '）', train_res)
    return train_res


# random.seed(8)
# random_index = random.sample(range(0, 2768), 40)
# random_index =["16153951.html"]

LTP_DATA_DIR = "/home/mm/Downloads/ltp_data_v3.4.0/"
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')

segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型

true_res_str = read_train_res()




def fill_table(path):

    # if index not in random_index:
    #     continue
    # list_true_res = re.findall(r'{}[^\n]+(?=\n)'.format(path.split(".")[0]), true_res_str)

    # text, entity_string = convert2txt('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/762567.html')
    text, entity_string = convert2txt('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/' + path)
    official_res_row = re.findall(r'{path}[^\n]+\n'.format(path = path.split(".")[0]),true_res_str)
    answer_dic = {"公告ID": path.split(".")[0]}
    _,asset_string , eval_string, money_string = entity_string.split("|||")

    entities_arrows_list = list(set([x if 'H&#~' in x else '' for x in re.split(r'\s', entity_string)]))
    short_name_list = [re.split(r"H&#~", x)[0]  for x in entities_arrows_list]
    reg_short_listr = ""
    for tiy in short_name_list:
        for tiny in re.split(r'[，、/]', tiy):
            if not re.search(r'(^公司$|^本公司$|环境$|^上市公司$|人$|资产|标的|交易|审计|对方|发行|对象|股东|对手|单位|事务所|计划|分公司|日$|董事|独立|书$|承诺|机构|评估|交所|股|认购|局$|律|本次|国家|中央|中国|重组|重大|期$|^元$|^万元$|^亿元$|《|》|股份|股分|利润|报告)', tiny):
                reg_short_listr += tiny
                reg_short_listr += "|"
    reg_short_listr = re.sub(r'^\||\|$', "", reg_short_listr)
    reg_short_listr = re.sub(r'\|\|', "|", reg_short_listr)

    answer_dic["估值方法"] = collections.Counter(eval_string.split(" ")).most_common(1)[0][0]
    answer_dic["交易金额"] = collections.Counter(money_string.split(" ")).most_common(1)[0][0]
    answer_dic["交易标的"] = collections.Counter(asset_string.split(" ")).most_common(1)[0][0]
    answer_dic["标的公司"] = ''
    answer_dic["交易对方"] = ''

    for row in entities_arrows_list:
        if len(row) < 2:
            continue
        short, long = row.split('H&#~')
        list_splits_short = re.split(r'/|、', short)
        for short_split in list_splits_short:
            if re.match(r'交易对[手方]|发行对象|认购人', short_split):
                answer_dic["交易对方"] = long
            if re.match(r'标的公司|目标公司', short_split):
                answer_dic["标的公司"] = long
                if "、" in long:
                    """ltp 识别实体， 针对顿号分开的pos，分别确认不含有动词副词，
                        然后在entity——string里面找相应的各自的股权信息/资产信息"""
                    asset_list = []
                    for long_split in long.split("、"):
                        # print("{} long_split is {}".format(path, long_split))
                        # asset_related_target = re.findall(r'{}[\d.%]+的?股[权分]|全部[股债分权]'.format(long_split), entity_string)
                        # if len(asset_related_target) > 0:
                        #     asset_list.append(re.findall(r'[\d.%]+的?股[权分]|全部[股债分权]', asset_related_target[0])[0])
                        # else:
                        if re.findall(r'{ls}[\d.%]+的?[股债分权份]{{2}}|{ls}全部的?[股债分权份资产负利和与]{{2,6}}'.format(ls=long_split), text) \
                                and re.findall(r'[\d.%]+的?[股债分权份资产负利和与]{2， 5}|全部的?[股债分权份资产负利和与]{2,6}', \
                                               re.findall(r'{ls}[\d.%]+的?股股债分权份资产负利和与]{{2,6}}|全部[股债分权份资产负利和与]{{2,6}}'.format(ls = long_split), text)[0]):
                        # asset_related_target = re.findall(r'{}[\d.%]+的?股[权分]|全部[股债分权]'.format(long_split), text)
                            asset_list.append(re.findall(r'[\d.%]+的?[股债分权份]{2}|全部的?[股债分权份资产负利和与]{2,6}',\
                                                         re.findall(r'{ls}[\d.%]+的?[股债分权份]{{2,4}}|全部的?[股债分权份资产负利和与]{{2,5}}'.format(ls =long_split), text)[0])[0])

                    answer_dic["交易标的"] = '|'.join(asset_list)
                    answer_dic["标的公司"] = "|".join(long.split("、"))

        if re.match(r'本次交易|交易标的|标的资产|交易资产|目标资产|标的股权', short_split):
            if re.findall(r'[\d.%]+的?[股债分权份]{2}|全部的?[股债分权份]{2}', long):
                list_ass = re.findall(r'[\d.%]+的?[股债分权份]{2}|全部的?[股债分权份]{2}', long)
                # if len(list_ass) > 1:
                answer_dic["交易标的"] = '|'.join(list_ass)
                list_tar = re.findall(r'({ls})(?=的?[\d.%]+的?[股债分权份]{{2,3}}|全部的?[股债分权份资产负利和与]{{2,6}})'.format(ls = reg_short_listr), long)
                answer_dic["标的公司"] = '|'.join(list_tar)

    if answer_dic["标的公司"]=="":
        guess_target = collections.Counter(re.findall(r'{ls}'.format(ls = reg_short_listr), entity_string)).most_common(8)
        for  tar in guess_target:
            if len(tar[0]) > 2:
                answer_dic["标的公司"] = guess_target
                pass

    # print(re.findall(r'(?<=[和及、，~的])[^\d和及、，~的股份分权]+(?=[\d.%的]+股[权分份])', entity_string))

    if answer_dic["标的公司"] =="":
        for post_fix  in  re.findall(r'(?<=[和及、，~的])[^\d和及、，~的股份分权资产负利与]+(?=的?[\d.%]+的?[股债分权份]{{2,3}}|全部的?[股债分权份资产负利和与]{{2,6}})', entity_string):
            if len(post_fix) in [3, 4, 5, 6]:
                answer_dic["标的公司"] = post_fix

    if answer_dic["标的公司"] != "" and answer_dic["交易标的"] != "":
        print("answer dict is ok ")
    else:
        print("fuck it {}".format(path))
    #                 # 说明交易
    #
    # # if "|" in answer_dic['标的公司'] and "|" not in answer_dic['交易标的']:
    # #     answer_dic['交易标的'] == ""
    # #     for target_split in re.split(r'|', answer_dic['标的公司']):
    # #         answer_dic['交易标的'] += re.findall()
    #
    #         if re.match(r'交易标的|标的资产|标的股权|目标资产', short_split):
    #             # if len(answer_dic['交易标的'])>1 and answer_dic['交易标的'] in long:
    #             #     print("股权最频的信息就在交易标的名词解释中{}".format(path))
    #             if re.search(r'的?[\d.%全部]+股[权分份]]', long):
    #                 answer_dic["标的公司"] ="|".join(re.split(r'的?[\d.%全部的]+股[权分份]、?', long))
    #                 answer_dic["交易标的"] ="|".join(re.findall(r'[\d.%全部的]+股[权分份]]', long))
    #             # elif len(answer_dic['交易标的'])>1:
    #             #     answer_dic['交易标的'] = re.findall(r'([\d.]+%的?(?:股权|股份|权益))', long)[0]
    submit_string = ''
    if '|' in str(answer_dic):
        target_list = answer_dic["标的公司"].split("|")
        asset_list = answer_dic["交易标的"].split("|")
        rows_to_gen = max(len(target_list), len(asset_list))
        for row in range(rows_to_gen):
            index_target = row if len(target_list) < row + 1  else len(target_list)-1
            index_asset = row if len(asset_list) < row + 1 else len(asset_list)-1
            submit_string += answer_dic["公告ID"]+ "\t" + asset_list[index_asset] \
                        + "\t" + target_list[index_target] + "\t" + answer_dic["交易对方"] \
                        + "\t" + answer_dic["交易金额"] + "\t" + answer_dic["估值方法"] + "\n"
    else:
        submit_string =  answer_dic["公告ID"]+ "\t" + answer_dic["交易标的"] \
                        + "\t" + answer_dic["标的公司"] + "\t" + answer_dic["交易对方"] \
                        + "\t" + answer_dic["交易金额"] + "\t" + answer_dic["估值方法"] + "\n"

    return submit_string



def write_txt():

    results_list = []


    for  path  in os.listdir('/home/mm/FDDC_datasets_dir/FDDC_announcements_round2_train_html/')[:10]:
        print("It comes {}".format(path))

        try:
            sub_str = fill_table(path)
            results_list.append(sub_str)
        except Exception as e:
            print("sth wrong with {}".format(path))
    pickle.dump(results_list, open("/home/mm/Documents/result_chongzu.pkl", 'wb'))


    if os.path.exists("chongzu.txt"):
        os.remove("chongzu.txt")
    for line in results_list:
        # print("8888888888888888888888")
        # print(dicti["公告ID"])
        # print(dicti["交易标的"])
        # print(dicti["标的公司"])
        # print(dicti["交易对方"])
        # print(dicti["交易金额"])
        # print(dicti["估值方法"])

        with open("chongzu.txt", 'a') as af:
             af.write(line)
            # if len(dicti["交易标的"].split("|"))==len(dicti["标的公司"].split("|")):
            #     for i in range(len(dicti["标的公司"].split("|"))):
            #         line_to_append =dicti["公告ID"]+ "\t" + dicti["交易标的"].split("|")[i] + "\t" + dicti["标的公司"].split("|")[i] + "\t" + dicti["交易对方"] + "\t" + dicti["交易金额"] + "\t" + dicti["估值方法"] + "\n"
            #         af.write(line_to_append)
            # elif len(dicti["交易标的"].split("|")) < len(dicti["标的公司"].split("|")):
            #     for i in range(len(dicti["标的公司"].split("|"))):
            #         line_to_append =dicti["公告ID"]+ "\t" + dicti["交易标的"].split("|")[i] + "\t" + dicti["标的公司"].split("|")[i] + "\t" + dicti["交易对方"] + "\t" + dicti["交易金额"] + "\t" + dicti["估值方法"] + "\n"
            #         af.write(line_to_append)

def eval():

    with open("chongzu.txt", 'r') as rf:
        for submit_row in rf:
            try:
                list_true_res = re.findall(r'{}[^\n]+(?=\n)'.format(submit_row.split("\t")[0]), true_res_str)
                for res_row in list_true_res:
                    if res_row == submit_row[:-1]:
                        print("well_done")
                    elif res_row.split("\t")[:3]==submit_row.split("\t")[:3]:
                        print("well_done for mainkey")
                    else:
                        print("badddd")
                        print(res_row)
                        print(submit_row[:-1])
                        print("bbbbbb")
            except Exception as e:
                print("baddd")
                print("the exception is {}".format(e))



if __name__=="__main__":
    write_txt()
    eval()