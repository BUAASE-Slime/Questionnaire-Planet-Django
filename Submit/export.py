

from Qn.models import *
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx import *
from io import BytesIO

import djangoProject.settings







def paper_to_docx(qn_id):
    document = Document()
    survey = Survey.objects.get(survey_id=qn_id)
    docx_title = survey.title + '_' + str(survey.username) + '_' + str(qn_id)+"考卷" + ".docx"

    print(docx_title)

    # run = document.add_paragraph().add_run('This is a letter.')
    # font = run.font
    # font.name = '宋体' 英文字体设置
    document.styles.add_style('Song', WD_STYLE_TYPE.CHARACTER).font.name = '宋体'  # 添加字体样式-Song
    document.styles['Song']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    # document.add_paragraph().add_run('第二个段落，abcDEFg，这是中文字符', style='Song')

    document.add_heading(survey.title, 0)


    paragraph = document.add_paragraph().add_run(survey.description, style='Song')
    introduction = "本考卷已经收集了" + str(survey.recycling_num) + "份，共计" + str(survey.question_num) + "个问题"
    paragraph = document.add_paragraph().add_run(introduction, style='Song')


    questions = Question.objects.filter(survey_id=survey)
    i = 1
    for question in questions:

        type = question.type
        type_str = ""
        if type == 'radio':
            type_str = "单选题"
        elif type == 'checkbox':
            type_str = '多选题'
        elif type == 'text':
            type_str = '填空题'
        elif type == 'mark':
            type_str = '评分题'
        elif type == 'judge':
            type_str = "判断题"
        document.add_paragraph().add_run(str(i) + "、" + question.title + "(" + type_str +"  "+ str(question.point)+"分 )", style='Song')

        i += 1
        options = Option.objects.filter(question_id=question)
        option_option = 0
        num = 1
        for option in options:
            option_str = "      "

            alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

            if question.type in ['checkbox', 'radio']:
                option_str += alphas[option_option] + " :  "
                # option_str += "选项 " + str(num) + " :  "
                option_option += 1
                num += 1

            option_str += option.content
            document.add_paragraph().add_run(option_str, style='Song')
        if question.type in ['mark', 'text']:
            document.add_paragraph(' ')

    document.add_page_break()
    # document.add_paragraph(str(qn_id))
    f = BytesIO()
    save_path = docx_title

    document.save(f)
    # document.save(save_path)

    docx_path = djangoProject.settings.MEDIA_ROOT + "\Document\\"
    from .views import IS_LINUX
    if IS_LINUX:
        docx_path = djangoProject.settings.MEDIA_ROOT + "/Document/"

    print(docx_path)
    document.save(docx_path + docx_title)

    return document, f, docx_title, docx_path