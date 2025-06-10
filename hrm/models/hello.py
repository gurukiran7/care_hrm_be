from django.db import models

from care.utils.models.base import BaseModel


class Hello(BaseModel):
    name = models.CharField(max_length=10)
