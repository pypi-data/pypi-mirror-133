import uuid
from django.db import models
from datetime import timedelta
from django.utils import timezone
from .management.setting import Base
from .management.helper import randomString


class RedjCaptchaModel(models.Model):
    id = models.UUIDField(
        unique=True,
        editable=False,
        primary_key=True,
        default=uuid.uuid4,
    )
    text = models.CharField(max_length=12)
    created_by = models.UUIDField(null=True, editable=False)
    deleted_at = models.DateTimeField(null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-created_at']
        db_table = "redj_captchas"

    def __str__(self):
        return str(self.id)

    def create():
        set_int = True
        set_str = True
        if Base.type == "str":
            set_str = True
            set_int = False
        if Base.type == "int":
            set_int = True
            set_str = False

        text = randomString(Base.size, set_int=set_int, set_str=set_str)
        model = RedjCaptchaModel.objects.create(
            text=text
        )
        return model

    def checkCaptcha(key, value):
        expier_at = timezone.now() + timedelta(seconds=int(Base.timeout))
        model = RedjCaptchaModel.objects.filter(
            id=key,
            text=value,
            deleted_at=None,
            created_at__lt=expier_at
        )
        return len(model) > 0
