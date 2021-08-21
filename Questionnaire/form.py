from django import forms

class SurveyIdForm(forms.Form):
    qn_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class QuestionIdForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class OptionIdForm(forms.Form):
    option_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))