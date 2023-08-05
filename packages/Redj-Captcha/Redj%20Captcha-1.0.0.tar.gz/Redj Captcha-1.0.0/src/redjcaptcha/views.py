from .models import RedjCaptchaModel
from .management.setting import Base
from django.http import JsonResponse
from .management.helper import generateImage


def getCaptcha(request):
    model = RedjCaptchaModel.create()
    image = generateImage(model.text)

    return JsonResponse({
        "image": image,
        "key": model.id,
        "timeout": Base.timeout,
        "created_at": model.created_at,
    })


def checkCaptcha(key, value):
    if Base.debug == True:
        return True
    return RedjCaptchaModel.checkCaptcha(key, value)
