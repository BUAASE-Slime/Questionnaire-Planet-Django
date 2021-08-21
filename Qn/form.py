from django import forms


class CollectForm(forms.Form):
    survey_id = forms.IntegerField()
