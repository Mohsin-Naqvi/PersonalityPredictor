from django import forms
# from .models import uploadResumeModel

class uploadResumeModelForm(forms.ModelForm):
    class Meta:
        # model = uploadResumeModel
        fields = ('file',)