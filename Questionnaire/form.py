from django import forms

class SurveyIdForm(forms.Form):
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class QuestionIdForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class OptionIdForm(forms.Form):
    option_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class CreateNewQnForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label="标题", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtitle = forms.CharField(label="副标题", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # direction = forms.CharField(label="简介", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
