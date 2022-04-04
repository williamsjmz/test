from geco.models import User
from django.db import models



# Portal's design
class Design(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='design')
  url = models.CharField(max_length=50)

  def __str__(self):
    return f'{self.url}'



# Pages
class Page(models.Model):

  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
  title = models.CharField(max_length=14)
  body = models.TextField(max_length=500)
  design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='pages')
  active = models.BooleanField(default=False)

  def __str__(self):
    return f'{self.title}'

