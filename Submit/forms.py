from django import forms

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

class SubmitIDForm(forms.Form):
    submit_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class CrossAnalysisForm(forms.Form):
    question_id_1 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    question_id_2 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))