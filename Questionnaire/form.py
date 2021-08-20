from django import forms

class SurveyIdForm(forms.Form):
    survey_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))