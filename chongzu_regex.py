import re, os
from htmlconvert2text import convert2txt
import  collections
import random

random_index = random.sample(range(0,2768), 6)

def read_train_res():
    with open('/home/47_7/Documents/aliyun-FDDC-2018-Financial-Challenge-/chongzu.train') as rf:
        train_res = rf.read()
        train_res = re.sub(r'\(', '（', train_res)
        train_res = re.sub(r'\)', '）', train_res)
    return train_res
def fill_table():
    resutl_text = ""
    results_list = []
    for index, path  in enumerate(os.listdir('/home/47_7/FDDC_datasets_dir/FDDC_announcements_round2_train_html/')) :
        if index not in random_index:
            continue
        print("It comes {}".format(path))
        # text, entity_string = convert2txt('/home/47_7/FDDC_datasets_dir/FDDC_announcements_round2_train_html/762567.html')
        text, entity_string = convert2txt('/home/47_7/FDDC_datasets_dir/FDDC_announcements_round2_train_html/' + path)
        answer_dic = {"公告ID": path.split(".")[0]}
        _,asset_string , eval_string, money_string = entity_string.split("|||")
        entities_arrows_list = list(set([x if '~' in x else '' for x in re.split(r'\s', entity_string)]))
        answer_dic["估值方法"] = collections.Counter(eval_string.split(" ")).most_common(1)[0][0]
        answer_dic["交易金额"] = collections.Counter(money_string.split(" ")).most_common(1)[0][0]
        answer_dic["交易标的"] = collections.Counter(asset_string.split(" ")).most_common(1)[0][0]
        for row in entities_arrows_list:
            # 如果在左侧的，是简称，里面有交易对手等称呼，则取右边的。
            if len(row) < 2:
                continue
            # print(row)
            short, long = row.split('H&#~')
            list_splits_short = re.split(r'/|、', short)
            for short_split in list_splits_short:
                if re.match(r'交易对[手方]|发行对象|认购人', short_split):
                    answer_dic["交易对方"] = long
                if re.findall(r'标的公司|目标公司', short_split):
                    answer_dic["标的公司"] = long
                if re.findall(r'交易标的|标的资产|标的股权|目标资产', short_split):
                    if len(answer_dic['交易标的'])>1 and answer_dic['交易标的'] in long:
                        print("股权最频的信息就在交易标的名词解释中{}".format(path))
                    # elif len(answer_dic['交易标的'])>1:
                    #     answer_dic['交易标的'] = re.findall(r'([\d.]+%的?(?:股权|股份|权益))', long)[0]

        results_list.append(answer_dic)
    if os.path.exists("chongzu.txt"):
        os.remove("chongzu.txt")
    for dicti in results_list:
        print(dicti["公告ID"])
        with open("chongzu.txt", 'a') as af:

            af.write(dicti["公告ID"]+ "\t" + dicti["交易标的"] + "\t" + dicti["标的公司"] + "\t" + dicti["交易对手"] + "\t" + dicti["交易金额"] + "\t" + dicti["估值方法"] + "\n")
def eval():
    official_res_string = read_train_res()

    with open("chongzu.txt", 'r') as rf:
        submit = rf.read()
    well_done = 0
    for row in  re.findall(r'{}[^\n](?=\n)', official_res_string):
        submit_row = re.findall(r'{}[^\n](?=\n)'.format(row.split("\t")[0]), submit)[0]
        if row == submit_row:
            print("well done")
            well_done += 1
    print(well_done)


if __name__=="__main__":
    try:
        fill_table()
    except Exception as e:
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{}".format(e))
    eval()