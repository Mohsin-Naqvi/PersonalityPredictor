from django.db import models

# Create your models here.
class uploadResumeModel(models.Model):
    # title = models.CharField(max_length=255, blank=True)
    file = models.FileField()
    # uploaded_at = models.DateTimeField(auto_now_add=True)