# 问卷星球

[![python3.8](https://img.shields.io/badge/python-%3E%3D3.8-brightgreen)](https://www.python.org/)  [![django3.2](https://img.shields.io/badge/django-3.0-blue)](https://docs.djangoproject.com/en/3.2/releases/3.2/)

> 北航 1921 软件工程暑期实践 满分项目 ~~万一有更多star呢~~

前端：[https://github.com/ZewanHuang/Questionnaire-Planet](https://github.com/ZewanHuang/Questionnaire-Planet)

## 项目介绍

问卷星球，问卷发布平台，实现了含普通问卷、考试问卷、报名问卷、投票问卷、疫情打卡问卷等五类问卷的创建、编辑、发布、统计功能。

项目突出特点有：

- 友好的问卷制作界面：空白问卷模板、大纲题目可拖拽编辑题目顺序、编辑问卷时每隔1分钟自动保存
- 特别问卷的展示与设计： 
  - 考试问卷显示**截止时间倒计时、且题目乱序展示**； 
  - 投票、考试问卷填报完成后展示答题反馈；
  - 疫情打卡可获取用户IP地址进行定位；
  - 报名问卷剩余名额的实时反馈，以及同步提交的数据库事务处理
- 完整实用的数据统计分析（含**图表分析与交叉分析**）
- 各类问卷与数据导出文件的**DIY设计**
- **逻辑关联问题**设计
- 支持上传小型**图片和视频**

## 运行环境

Python 3.8 及以上

Django 3.0 及以上

安装第三方依赖库,请根据操作系统类型在项目根目录下使用以下命令安装

```
pip install -r requirements.txt 
<!-- windows -->
pip install -r requirements_linux.txt 
<!-- linux -->
```
此外，若您想将此项目部署至linux，还需再linux上安装`Libreoffice`，并安装宋体字体，以问卷导出pdf使用。否则使用相应功能会出现问题。本项目中使用`Libreoffice`的位置为`/Submit/export.py/doc2pdf_linux`中依此命令导出pdf，若您安装的Libreoffice 版本不为7.0 也请对应修改版本号。而windwos与linux所需依赖不同也就在pdf导出上面，其余全部相同。

```powershell
cmd = 'libreoffice7.0 --headless --invisible  --convert-to pdf:writer_pdf_Export'.split() + [docPath] + ['--outdir'] + [pdfPath]
```



## 如何使用

> 须结合 [前端说明](https://github.com/ZewanHuang/Online-Publish-Django) 进行配置

运行项目前，请根据文件内容提示修改 **utils/secrets.py**，其中包含前端路由 `webFront`、后端路由 `webBack`，数据库基本信息 `DataBase`  和基本邮箱信息`Email`。 如需连接其他类型的数据库也请对应修改`utils/secrets.py `的内容

而后使用`python manage.py makemigrations`   和 `python manage.py migrate`  生成对应数据库文件

本地运行项目，使用`python manage.py runserver`运行本项目，由于前后端的分离性，可以结合前端项目来运行此项目

## 基本页面展示

欢迎主页

![welcome](https://github.com/ZewanHuang/Questionnaire-Planet/blob/master/src/assets/images/home.png)

管理中心

![center](https://github.com/ZewanHuang/Questionnaire-Planet/blob/master/src/assets/images/center.png)

编辑界面

![edit](https://github.com/ZewanHuang/Questionnaire-Planet/blob/master/src/assets/images/edit.png)

填写界面

![publish](https://github.com/ZewanHuang/Questionnaire-Planet/blob/master/src/assets/images/publish.png)

统计界面

![statistic](https://github.com/ZewanHuang/Questionnaire-Planet/blob/master/src/assets/images/statistic.png)



# 其他



由于此项目在开发后进行了一次**未经测试**的大规模项目结构重构，实际运行时可能会遇到一些依赖问题，欢迎在遇到问题时使用Email或Issue联系我们。
