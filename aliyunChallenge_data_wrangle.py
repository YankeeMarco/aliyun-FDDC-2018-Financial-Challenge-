

with open(r"/home/mm/Downloads/round1_train_20180518/hetong/hetong.train","r") as rfile:

    count=0
    while count<1000:
        line=rfile.readline()
        count+=1
        if len(line.split("\t"))==7:
            print("7, the row is {}".format(count))
        elif len(line.split("\t"))==8:
            print("8, the row is {}".format(count))
        else :
            print("aha {}, the row is {}".format(len(line.split("\t")),line))

cd /home/mm/aliyunChallenge/ import re, os ,html2text pattern = re.compile(r"[^。]+交易对方[^。]+。") notin = 0 for i in os.listdir("/home/mm/FDDC_datasets_dir/FDDC_announcement_round2_chongzu_pdf"): lll = re.findall(pattern, convert2txt("/home/mm/FDDC_datasets_dir/FDDC_announcement_round2_chongzu_pdf/"+i,)) lent = len(lll) if lent > 0: print(lll[0]+" "+str(lent)) else: print("8888888888888888888 "+i) notin +=1

import re, os ,html2text
pattern = re.compile(r"[^。|]+交易对方[^。|]+元[^。|]?。")
notin = 0
for i in os.listdir("/home/mm/FDDC_datasets_dir/FDDC_announcement_round2_chongzu_pdf"):
    lll = re.findall(pattern, convert2txt("/home/mm/FDDC_datasets_dir/FDDC_announcement_round2_chongzu_pdf/"+i,))
    lent = len(lll)
    if lent > 0:
        print(lll[0]+"         "+str(lent))
    else:
        print("8888888888888888888    "+i)
        notin +=1

pattern = re.compile(r"[^。]+交易对方[^。]+。")
...: notin = 0
...: for i in os.listdir("/home/html/"):
    ...:     lll = re.findall(pattern, convert2txt("/home/html/" + i, ))
...:     lent = len(lll)
...:     if lent > 0:
    ...:         print(lll[0] + "         " + str(lent))
...: else:
...:         print("8888888888888888888    " + i)
...:         notin += 1



for i in os.listdir('/home/html/')[0:2770:50]:
    ...:     with open('/home/html/'+i, 'r') as rf:
    ...:         ss = rf.read()
    ...:         if '交易概' in ss and '具体方案' in ss:
    ...:             print("222222222    {}".format(i))
    ...:         elif '具体方案' in ss and '交易概' not in ss:
    ...:             print('具体方案 {}'.format(i))
    ...:         elif '交易概' in ss and '具体方案' not in ss:
    ...:             print('交易概况 {}'.format(i))
    ...:         elif '交易对方为' in ss:
    ...:             print('交易对方为    {}'.format(i))
    ...:         else:
    ...:             print("NNNNNNNNNNN  {}".format(i))


list_keywords = ['交易概','具体方案','交易对方为','交易概','交易总金额','交易总金额','评估方法为']

list_keywords = ['交易概','具体方案','交易对方为','交易概况','交易总金额','
    ...: 交易总金额','评估方法为','资产置换标的']

for i in os.listdir('/home/html/')[0:2770:50]:
    ...:     with open('/home/html/'+i, 'r') as rf:
    ...:         ss = rf.read()
    ...:         dim_list = []
    ...:         for j in list_keywords:
    ...:             if j in ss:
    ...:                 dim_list.append(j)
    ...:         print(str(len(dim_list))+'   '+str(dim_list)+'     '+str(i))
    ...:
