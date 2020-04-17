# from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

# 그대로 활용하지 못하는 경우는 상속받아서 custom 하기!
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email']
