#coding=utf-8
import os
import codecs
import re

# with open('china_city_names.txt','r') as rf:
#     list_cities = rf.read().split("|")

def convert2txt(path1):
    with codecs.open(path1, 'r',encoding='utf-8',errors='stric') as  rrf:
        texx = rrf.read()
    """
        先把html中名词实体提取出来，做成列表返回给调用方， 例如：
            朝阳分公司
            /
            朝阳牛逼公司
          </td>
          <td>
           指
          </td>
          <td>
           北京数字天域科技股份有限公司朝阳分公司
           提取出来成为键值对，格式’朝阳分公司/朝阳牛逼公司~北京数字天域科技股份有限公司朝阳分公司‘
    """
    # 先将html中的回车空格等等符号去掉
    texx = re.sub(r'[\s\n]', r'', texx)  # 把html中所有空格回车去掉，防止文档差错，表格的数据信息不要了，此任务不需要
    list_entity = re.findall(r'(?<=>)[^<>]+[></a-z]+指[></a-z]+[^<>]+', texx)
    # list_entity = re.findall(r'<td>[^<>]+</td><td>指</td><td>[^<>]+</td>',texx) # 很容易找出实体指代部分了
    # list_money = re.findall(r'(\d{5,12})(?=元)', texx)
    list_target = re.findall(r'([\d.]+%的?(?:股权|股份|权益))',texx)
    list_eval_way = re.findall(r'(市场法、重置成本法|市场法|成本法|资产基础法、市场比较法|收益现值法|成本加和法|折现现金流量法|内含价值调整法|市场法、收益法|资产基础法、市场法|成本法、收益法|可比公司市净率法|收益法、重置成本法|成本发、市场法、收益法|收益法、资产基础法|成本加和法、收益现值法|重置成本法|单项资产加和法|成本逼近法|收益法、市场法|资产基础法、收益法|市场比较法、成本逼近法|收益现值法、成本加和法|收益现值法、资产基础法|单项资产加总法|收益法|假设清偿法|收益法、市场比较法|收益还原法|现金流量法|收益法、基础资产法|现金流折现法|市场比较法|收益法、成本法|重置成本法、市场比较法|市场比较法、收益法|收益现值法、重置成本法|资产基础法、成本法|成本法、市场法、收益法|基准地价修正法、市场比较法|估值法|成本法、市场法|成本逼近法、市场比较法|基础资产法|资产基础法)',texx)
    entity_string = ''

    for i in list_entity:
        first = i.split("</")[0]
        third = i.split(">")[-1]
        entity_string+=first
        entity_string+='H&#~'
        entity_string+=third
        entity_string+=' '
    entity_string += "|||"
    for i in list_target:
        entity_string += i
        entity_string += ' '
    entity_string += "|||"
    for i in list_eval_way:
        entity_string += i
        entity_string += ' '
    entity_string += "|||"



    texx = re.sub(r'<[^<>]+>', r'\n', texx) # 把所有html标签换成一对空格，多了很多换行符,有嵌套标签，需要再删一遍
    texx = re.sub(r'<[^<>]+>', r' ', texx)

    # secnames_dicts = re.findall(r'[\s\n]?[\u4e00-\u9fcc，a-zA-Z.、/（）0-9]+[\s\n]+指[\s\n]+[\u4e00-\u9fcc，a-zA-Z.、/（）0-9]+[\s\n]?',texx)
    #
    # for i in secnames_dicts:
    #     secname, fullname = re.split(r'[\s\n]+指[\s\n]+', i)
    #     entity_string += re.sub(r'[\n\s]', '', secname) + "~" + re.sub(r'[\n\s]', '', fullname) + ' '


    texx = re.sub(r'(?<=\d),(?=\d[^股]{8})', '', texx) # 把金额中间的逗号去掉,股份的数字不能去掉逗号
    texx = re.sub(r'(?<=[^.][^.][^.][^.][^.][^.]\d)万(?=元|美元|欧元)','0000', texx) # 把小数点后两位的万换成
    texx = re.sub(r'(?<=(\.\d))(?!\d)万(?=元|美元|欧元)','000犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d))(?!\d)万(?=元|美元|欧元)','00犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d\d))(?!\d)万(?=元|美元|欧元)','0犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d\d\d))(?!\d)万(?=元|美元|欧元)','犇畚', texx)

    texx = re.sub(r'(?<=[^.][^.][^.][^.][^.][^.][^.][^.]\d)亿(?=元|美元|欧元)','00000000', texx) # 把小数点后面的亿元换成
    texx = re.sub(r'(?<=(\.\d))(?!\d)亿(?=元|美元|欧元)','0000000犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d))(?!\d)亿(?=元|美元|欧元)','000000犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d\d))(?!\d)亿(?=元|美元|欧元)','00000犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d\d\d))(?!\d)亿(?=元|美元|欧元)','0000犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d\d\d\d))(?!\d)亿(?=元|美元|欧元)','000犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d\d\d\d\d))(?!\d)亿(?=元|美元|欧元)','0犇畚', texx)
    texx = re.sub(r'(?<=(\.\d\d))(?!\d\d\d\d\d\d\d)亿(?=元|美元|欧元)','犇畚', texx)

    texx = re.sub(r'(?<=\d)\.(?=\d+犇畚)','',texx) # 去掉残留的小数点
    texx = re.sub(r'犇畚', '', texx)  # 把单位改回来
    texx = re.sub(r'(\n+指\n+|指\n)', ' 指 ', texx) # 把“指”两边多余的换行符去掉
    texx = re.sub(r'[\s\n]+', ' ', texx) # 把可能产生的连续空格换成一个空格，应该没有执行啥吧
    # texx = re.sub(r'\n+', ' ', texx) # 把连续的换行全部换成一个空格
    # html文件中普遍有一个乱码：ft 是汉字的山
    texx = re.sub(r'ft', r'山', texx)
    # 英文半角括号换成汉语全角括号，以防正则bug
    texx = re.sub(r'\(','（', texx)
    texx = re.sub(r'\)', '）', texx)
    texx = re.sub(r'([^屄])\1{10, 200}', ' ', texx)
    list_money = re.findall(r'(\d{5,12})(?=元)', texx)
    for i in list_money:
        entity_string += i
        entity_string += ' '
    return texx, entity_string


def conv_and_save(path1, path2):

    with open(path2,"w") as wf:
        wf.write(convert2txt(path1))
if __name__=="__main__":
    source_path = r"/home/47_7/FDDC_datasets_dir/FDDC_announcements_round2_train_html/"
    out_path = r"/home/47_7/Documents/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/"
    for i in os.listdir(source_path)[0:2770:50]:

        text, entity_string = convert2txt("/home/47_7/FDDC_datasets_dir/FDDC_announcements_round2_train_html/1058852.html")
        text, entity_string = convert2txt(source_path+i)
        with open(out_path+"text"+i.split(".")[0], "w") as f:
             f.write(text)
        with open(out_path+"entity"+i.split(".")[0], "w") as f:
             f.write(entity_string)




