from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from djangoProject.settings import WEB_ROOT
from resources.form import ImageForm, VideoForm
from resources.models import ImageModel, VideoModel


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        _imageForm = ImageForm(request.POST, request.FILES)
        if _imageForm.is_valid():
            image = _imageForm.cleaned_data.get('image')
            if image.name.split('.')[-1] not in ['jpeg', 'jpg', 'png', 'bmp', 'tif', 'gif']:
                return JsonResponse({'status_code': 2, 'message': '图片格式有误'})

            _imageInstance = ImageModel(instance=image)
            _imageInstance.save()

            _imageName = _imageInstance.instance.name.split('/')[-1]
            _imageUrl = WEB_ROOT + _imageInstance.instance.url
            return JsonResponse({
                'status_code': 1,
                'name': _imageName,
                'url': _imageUrl
            })

        return JsonResponse({'status_code': -1})
    return JsonResponse({'status_code': -2})


@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        _videoForm = VideoForm(request.POST, request.FILES)
        if _videoForm.is_valid():
            video = _videoForm.cleaned_data.get('video')
            if video.name.split('.')[-1] not in ['wmv', 'mp4', 'flv', 'mkv']:
                return JsonResponse({'status_code': 2})

            _videoInstance = VideoModel(instance=video)
            _videoInstance.save()

            _videoName = _videoInstance.instance.name.split('/')[-1]
            _videoUrl = WEB_ROOT + _videoInstance.instance.url
            return JsonResponse({
                'status_code': 1,
                'name': _videoName,
                'url': _videoUrl
            })

        return JsonResponse({'status_code': -1})
    return JsonResponse({'status_code': -2})
