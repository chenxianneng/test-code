from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
import chardet
import pickle
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import utils
import time
import os
from openpyxl import workbook
from openpyxl import load_workbook

def read_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf:
        # resource manager
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        laparams = LAParams()
        # device
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        process_pdf(rsrcmgr, device, pdf)
        device.close()
        content = retstr.getvalue()
        retstr.close()

        #fencoding = chardet.detect(content)
        #print(fencoding)
        # print(type(content), flush=True)
        # lines = str(content).split("\n")
        # return lines
        return str(content)

def re_find(key_word, content):
    try:
        str_list = list(key_word)
        temp = u'\s*'.join(str_list)
        findword = temp
        #print(findword)
        # pattern = re.compile(findword)
        # find_results = pattern.findall(content)

        # return find_results

        return re.findall(findword, content)
    except Exception as e:
        return []


def compare_pdf(contract_pdf_path, approval_pdf_path):
    company, product = None, None
    contract_content = read_pdf(contract_pdf_path)
    
    #findword = u'基金或本基金：(.*)'
    findword = u'基金或本基金：指([\s\S]*?)2'
    pattern = re.compile(findword)
    results = pattern.findall(contract_content)
    print(results)

    if len(results) != 0:
        findword = results[0].strip()
        approval_content = read_pdf(approval_pdf_path)
        #print(approval_content)
        str_list = list(findword)
        temp = u'\s*'.join(str_list)
        findword = temp
        #print(findword)
        results = re.findall(findword, approval_content)
        print(results)
        if len(results) != 0:
            product = results[0].strip()

    findword = u'基金管理人：指(.*)'
    pattern = re.compile(findword)
    results = pattern.findall(contract_content)
    if len(results) != 0:
        company = results[0].strip()
        print(company)

    return company, product

company, product = compare_pdf('D:/IPA/external/基金对比资料/基金对比资料/广发9只基金/广发中证军工ETF联接C/基金合同.pdf', \
    'D:/IPA/external/基金对比资料/基金对比资料/广发9只基金/广发中证军工ETF联接C/招募说明书201801.pdf')

def run(company, product, code):  
    template_path = utils.get_working_dir() + '/template.xlsx'
    w_workbook = load_workbook(template_path)
    sheets = w_workbook.sheetnames
    w_sheet = w_workbook[sheets[0]]

    w_sheet.cell(row = 6, column = 2).value = product.replace(" ", "").replace("\n", "")
    content = '合规审查意见（法律合规部填写）：\n \n   根据业务侧提供的相关资料，本产品无重大法律合规风险，合规意见如下：\n   \n    \
        一、本产品发行人为' + company + '，具有保监会颁发保险公司法人许可证，根据《关于规范商业银行代理销售业务的通知》（银监发2016[24]号）规定：商业银行可接受国务院证券监督管理机构管理并持有金融牌照的金融机构委托，在本行渠道向客户推介、销售合作机构依法发行的金融产品。\n      \n     \
        二、经业务侧尽调，可于银保监会网站查询该产品。属于依法发行的保险产品。\n\n     \
        三、合规提示\n    1.交互页面及关于产品功能的描述需经合作方确认；2.投诉、理赔需由合作方负责，并在合同中约定双方权责义务关系。\n    \n'
    w_sheet.cell(row = 7, column = 1).value = content

    date = time.strftime("%Y-%m-%d", time.localtime())
    w_sheet.cell(row = 19, column = 2).value = date

    save_path = utils.get_working_dir()  + '/合规评审表' + code + '(' + product + ')'
    w_workbook.save(save_path)