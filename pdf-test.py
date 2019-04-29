# import PyPDF2 
  
# # creating a pdf file object 
# pdfFileObj = open('d:/test.pdf', 'rb') 
  
# # creating a pdf reader object 
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
  
# # printing number of pages in pdf file 
# print(pdfReader.numPages) 
  
# # creating a page object 
# pageObj = pdfReader.getPage(5) 
  
# # extracting text from page 
# print(pageObj.extractText()) 
  
# # closing the pdf file object 
# pdfFileObj.close()

# import textract
# text = textract.process('d:/test.pdf', method='pdfminer')
# print(text)

from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
import chardet

 
def read_pdf(pdf):
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
    # 获取所有行
    #fencoding = chardet.detect(content)
    #print(fencoding)
    print(type(content), flush=True)
    lines = str(content).split("\n")
    return lines
 
 

with open('d:/test2.pdf', "rb") as my_pdf:
    lines = read_pdf(my_pdf)

    file_name = 'pdf.txt'
    #f = open(file_name, "w", encoding='gb18030')
    with open(file_name, "w", encoding='utf-8') as pdf_txt:
    #temp = content.encode('utf-8')
        for line in lines:
            pdf_txt.write(line)

    #print(read_pdf(my_pdf))

# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch, cm
# c = canvas.Canvas('ex.pdf')
# c.drawImage('ar.jpg', 0, 0, 10*cm, 10*cm)
# c.showPage()
# c.save()

# from fpdf import FPDF
 
# pdf = FPDF()
# pdf.add_page()
# pdf.set_font("Arial", size=12)
# pdf.cell(200, 10, txt="Welcome to Python!", ln=1, align="C")
# pdf.output("simple_demo.pdf")

# simple_table.py
 
# from fpdf import FPDF
 
# def simple_table(spacing=1):
#     data = [['First Name', 'Last Name', 'email', 'zip'],
#             ['Mike', 'Driscoll', 'mike@somewhere.com', '55555'],
#             ['John', 'Doe', 'jdoe@doe.com', '12345'],
#             ['Nina', 'Ma', 'inane@where.com', '54321']
#             ]
 
#     pdf = FPDF()
#     pdf.set_font("Arial", size=12)
#     pdf.add_page()
 
#     col_width = pdf.w / 4.5
#     row_height = pdf.font_size
#     for row in data:
#         for item in row:
#             pdf.cell(col_width, row_height*spacing,
#                      txt=item, border=1)
#         pdf.ln(row_height*spacing)
 
#     pdf.output('simple_table.pdf')
 
# simple_table()

# html2fpdf.py 
from fpdf import FPDF, HTMLMixin
 
class HTML2PDF(FPDF, HTMLMixin):
    pass
 
def html2pdf():
    html = '''<h1 align="center">PyFPDF HTML Demo</h1>
    <p>This is regular text</p>
    <p>You can also <b>bold</b>, <i>italicize</i> or <u>underline</u>
    '''
    pdf = HTML2PDF()
    pdf.add_page()
    pdf.write_html(html)
    pdf.output('html2pdf.pdf')
 
html2pdf()
