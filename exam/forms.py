from django import forms


class AnswerForm(forms.Form):
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


class URLForm(forms.Form):
    code = forms.CharField(label="问卷链接", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


class CollectForm(forms.Form):
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class FinishForm(forms.Form):
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    finish_time = forms.DateTimeField(input_formats=None)


class CreateNewQuestionForm(forms.Form):
    # username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label="标题", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direction = forms.CharField(label="副标题", max_length=256, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    must = forms.BooleanField(label="是否是必答")
    type = forms.CharField(label="类型", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    options = forms.CharField(label="选项", max_length=1024, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # 选项不可过长
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    raw = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label="行数")
    score = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}), label="得分")
    right_answer = forms.CharField(label="标准答案", max_length=128,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
