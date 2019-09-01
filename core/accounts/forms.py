#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
from accounts.backends import EmailBackend
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    '''
    check user credentials
    '''
    email = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        _password = self.cleaned_data.get('password')
        user = EmailBackend.authenticate(self, email=email, password=_password)
        if not user or not user.is_active:
            raise forms.ValidationError(_("Sorry, credentials are not valid. Please, try again."))
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        _password = self.cleaned_data.get('password')
        user = EmailBackend.authenticate(self, email=email, password=_password)
        return user