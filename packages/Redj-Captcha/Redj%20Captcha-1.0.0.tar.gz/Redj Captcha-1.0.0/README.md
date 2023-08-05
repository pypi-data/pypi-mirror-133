# Redj Captcha
Django / Rest Framework captcha

## Getting Started

> in `setting.py`:

```
INSTALLED_APPS = [
    ...
    'redjcaptcha',
]
```

> in `urls.py` and check `http://localhost:8000/captcha`:

```
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('redjcaptcha.urls')),
]
```

> check Captcha (django):
```
from redjcaptcha.setup import checkCaptcha

check = checkCaptcha(captcha_key, captcha_value)
if check==False:
    return 'inValid'
```

> check Captcha (rest_framework):
```
from rest_framework import serializers
from redjcaptcha.setup import checkCaptcha

class CaptchaSerializer(serializers.Serializer):
    captcha_key = serializers.CharField()
    captcha_value = serializers.CharField()

    def validate(self, data):
        check = checkCaptcha(data['captcha_key'], data['captcha_value'])
        if check==False:
            print('\n=====> Captcha faild')
            raise Exception()

        print('\n=====> Captcha success')
        return check
```

> change default setting:
```
from redjcaptcha.setup import init

init(
    size=6,
    debug=True,
    font_size=50,
    timeout=6000,
    type="str-int",
    image_height=70,
    image_weight=180,
    text_color="random",
    background_color="#fff"
)
```