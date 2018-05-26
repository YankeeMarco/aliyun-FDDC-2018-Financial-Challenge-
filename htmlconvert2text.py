# import nltk
# from bs4 import  BeautifulSoup
# html = "8677857.html"
# soup=BeautifulSoup(html)
# html_text = soup.get_text()
#
# raw = nltk.clean_html(html_text)
# print(raw)
import html2text
import html



def convert2txt(path):
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

        with open(path, "r") as rf:
            strtxt=rf.read()
        return h.handle(strtxt).replace('\n','').replace('\r','').replace('\t','').replace(' ','')
    except:
        raise Exception

def conv_and_save(path1, path2):
    with open(path2,"w") as wf:
        wf.write(convert2txt(path1))
if __name__=="__main__":
    print(convert2txt("/home/mm/aliyunChallenge/8677857.html"))
    with open("/home/mm/aliyunChallenge/test_convert2text.tex", "w") as f:
        f.write(convert2txt("/home/mm/aliyunChallenge/8677857.html"))
