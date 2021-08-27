from django import forms

from Qn.models import Question


class UploadPictureForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = 'image'
