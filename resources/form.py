from django import forms

from resources.models import ImageModel, VideoModel


class ImageForm(forms.Form):
    image = forms.ImageField(label='图片')

    class Meta:
        model = ImageModel
        fields = 'image'


class VideoForm(forms.Form):
    video = forms.FileField(label='视频')

    class Meta:
        model = VideoModel
        fields = 'video'
