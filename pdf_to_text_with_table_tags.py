import pdfplumber
import os,re
file_path = "/home/FDDC_announcements_round2_train_pdf/"

def  pdf_tbl2txt(file):
    pdf = pdfplumber.open(file_path + "my.pdf")
    for i in pdf.pages:
        # page = pdf.pages[0]
        # i.extract_table()
        if i.find_tables(table_settings={}):
            i.crop(boundiipng_box)