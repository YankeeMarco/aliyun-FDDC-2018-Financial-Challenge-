
import html2text
import os
import codecs

def convert2txt(path1):
    try:
        h = html2text.HTML2Text()
        h.ignore_images = True
        h.inline_links = False
        h.wrap_links = False
        h.unicode_snob = True  # Prevents accents removing
        h.skip_internal_links = True
        h.ignore_anchors = True
        h.body_width = 0
        h.use_automatic_links = True
        # print("hhhhh")
        with codecs.open(path1, 'r',encoding='utf-8',errors='stric') as  rrf:
            texx = rrf.read()
        # return h.handle(texx).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
        return h.handle(texx)
        # with open(path1, "rb") as rf:
        #     strtxt=rf.read().decode(encoding='utf-8')
        #     return h.handle(strtxt).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
    except Exception as e:
        print("the excepiton is {}".format(e))

def conv_and_save(path1, path2):

    with open(path2,"w") as wf:
        wf.write(convert2txt(path1))
if __name__=="__main__":
    # print(convert2txt("/home/mm/aliyunChallenge/8677857.html"))
    # os.mkdir("/home/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir")
    for i in os.listdir("/home/html/")[0:2770:50]:
        with open("/home/aliyun-FDDC-2018-Financial-Challenge-/test_text_dir/{}.text".format(i.split(".")[0]), "w") as f:
             f.write(convert2txt("/home/html/"+i))
             # print("wellllll")
