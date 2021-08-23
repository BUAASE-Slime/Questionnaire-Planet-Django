
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



# convert(os.getcwd()+"\\1.docx",os.getcwd()+"\\1.pdf")
doc2pdf_linux(os.getcwd()+"/hzh8.docx",os.getcwd())
