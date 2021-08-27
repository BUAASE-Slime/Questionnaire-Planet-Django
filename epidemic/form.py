from django import forms

from Qn.models import Question


class UploadPictureForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='图片')

    class Meta:
        model = Question
        fields = 'image'


class GetForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class UploadVideoForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    video = forms.FileField(label='视频')

    class Meta:
        model = Question
        fields = 'video'
