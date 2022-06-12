from django.db import models
from django.contrib.auth.models import User



class ToDo(models.Model):
    text = models.TextField("содержимое")
    is_done = models.BooleanField("ВЫполнено", default=False)
    owner = models.ForeignKey(
        User, models.CASCADE, blank=True, null=True,
        verbose_name="Хозяин",
    )

    def __str__(self) -> str:
        return str(self.text)
