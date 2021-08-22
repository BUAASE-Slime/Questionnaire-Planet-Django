from django import forms


class CollectForm(forms.Form):
    survey_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class AnswerForm(forms.Form):
    survey_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))

class URLForm(forms.Form):
    url = forms.CharField(label="问卷链接", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))

class UserNameForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))

class SurveyIdForm(forms.Form):
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class QuestionIdForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class OptionIdForm(forms.Form):
    option_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateNewQnForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label="标题", max_length=128,required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="简介", max_length=256,required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # direction = forms.CharField(label="简介", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.CharField(label="类型", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))

# username title direction is_must_answer type qn_id options
class CreateNewQuestionForm(forms.Form):
    # username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label="标题", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direction = forms.CharField(label="副标题", max_length=256,required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    must = forms.BooleanField(label="是否是必答")
    type = forms.CharField(label="类型", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    options = forms.CharField(label="选项", max_length=1024, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # 选项不可过长
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    raw = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}),label="行数")
    score = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}),label="得分")