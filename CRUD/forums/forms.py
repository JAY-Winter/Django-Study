from django import forms
from django import forms
from .models import Forum

class ForumForm(forms.ModelForm):
    
    class Meta:
        model = Forum
        fields = '__all__'
