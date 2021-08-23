
from docx.enum.style import WD_STYLE_TYPE
from  docx.oxml.ns import  qn
from docx import *
import os,sys
import subprocess

from docx2pdf import convert
def doc2pdf_linux(docPath, pdfPath):
    """
    convert a doc/docx document to pdf format (linux only, requires libreoffice)
    :param doc: path to document
    """


    cmd = 'libreoffice7.0 --headless --invisible  --convert-to pdf:writer_pdf_Export'.split() + [docPath] + ['--outdir'] + [pdfPath]
    print(cmd)
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout=30)
    stdout, stderr = p.communicate()
    if stderr:
        raise subprocess.SubprocessError(stderr)

import datetime

# convert(os.getcwd()+"\\1.docx",os.getcwd()+"\\1.pdf")
today_exact = datetime.datetime.now()
today = datetime.datetime(year=today_exact.year,month=today_exact.month,day=today_exact.day)
yesterday = today - datetime.timedelta(days=1)
a_week_age = today - datetime.timedelta(days=7)
day_list = []
for i in range(7,0,-1):
    the_day = today-datetime.timedelta(days=i)
    print(the_day)
    day_list.append(the_day)
print(today)