

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


    paragraph = document.add_paragraph().add_run("考试介绍： "+survey.description, style='Song')
    sum_score = 0
    questions = Question.objects.filter(survey_id=survey)
    for question in questions:
        sum_score += question.point
    introduction = "考试须知：本考卷共计" + str(survey.question_num) + "个问题，总分共计 "+str(sum_score)+"分"

    paragraph = document.add_paragraph().add_run(introduction, style='Song')

    warning = "此外本场考试的截止时间为：" + str(survey.finished_time) + "注意不要在考试截止时间后提交试卷！！"
    document.add_paragraph().add_run(warning, style='Song')
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

import xlwt

from Qn.views import KEY_STR
def write_exam_to_excel(qn_id):
    qn = Survey.objects.get(survey_id=qn_id)
    submit_list = Submit.objects.filter(survey_id=qn)

    xls = xlwt.Workbook()
    sht1 = xls.add_sheet("Sheet1")

    sht1.write(0, 0, "序号")
    sht1.write(0, 1, "提交者用户名")
    sht1.write(0, 2, "提交时间")
    question_list = Question.objects.filter(survey_id=qn)
    question_info_list = []; questions = []
    for question in question_list:
        if question.type in ['school','name','class','stuId']:
            question_info_list.append(question)
        else:# TODO 都是问题吧？
            questions.append(question)
    i = 1
    for question in question_info_list:
        sht1.write(0, 2 + i,  question.title)
        i += 1

    question_num = len(questions)
    info_num = len(question_info_list)
    # i = 1

    for question in questions:
        sht1.write(0, 2 + i, str(i-info_num) + "、" + question.title+" ("+str(question.point)+"分)")
        i += 1
    sht1.write(0, 2 + i, "总分")
    pattern_green = xlwt.Pattern()  # Create the Pattern
    pattern_green.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern_green.pattern_fore_colour = 3
    # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
    style_green = xlwt.XFStyle()  # Create the Pattern
    style_green.pattern = pattern_green # Add Pattern to Style

    pattern_red = xlwt.Pattern()  # Create the Pattern
    pattern_red.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern_red.pattern_fore_colour = 2
    # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
    style_red = xlwt.XFStyle()  # Create the Pattern
    style_red.pattern = pattern_red  # Add Pattern to Style

    id = 1
    for submit in submit_list:
        sht1.write(id, 0, id)
        username = submit.username
        if username == '' or username is None:
            username = "匿名用户"
        sht1.write(id, 1, username)
        sht1.write(id, 2, submit.submit_time.strftime("%Y/%m/%d %H:%M"))
        question_num = 1
        for question in question_info_list:
            answer_str = (Answer.objects.get(submit_id=submit, question_id=question)).answer
            sht1.write(id, 2 + question_num, answer_str)
            question_num += 1
        for question in questions:
            answer_str = ""
            try:
                answer = Answer.objects.get(submit_id=submit, question_id=question)
                answer_str = answer.answer
            except:
                answer_str = ""
            if question.type == 'checkbox':
                answer_str = answer_str.replace(KEY_STR,';')
            if answer.answer == question.right_answer:
                style = style_green
            else:
                style = style_red

            sht1.write(id, 2 + question_num, answer_str,style)

            question_num += 1
        sht1.write(id, 2 + question_num, submit.score)

        id += 1
    save_path = djangoProject.settings.MEDIA_ROOT + "\Document\\"
    from .views import IS_LINUX
    if IS_LINUX:
        save_path = djangoProject.settings.MEDIA_ROOT + "/Document/"
    excel_name = qn.title + "问卷的统计信息" + ".xls"
    xls.save(save_path + excel_name)
    return excel_name

