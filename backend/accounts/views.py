#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import View, RedirectView
#from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

# Create your views here.
class BaseWebMixin(LoginRequiredMixin, View):
    '''
    Redirect requests without an active session to login
    '''
    login_url = reverse_lazy('accounts:login')
    redirect_field_name = 'redirect_to'

class LoginView(View):
    '''
    GET: load form template to do login

    POST: receive login credentials, validate it and returns
    an active session, with permissions or a message
    '''
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if request.POST and form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                request.session['user_perms'] = [x.codename \
                    for x in user.user_permissions.all()]
                return HttpResponseRedirect("web/index.html")   # Redirect to a success page.
        return render(request, 'accounts/login.html', {'form': form })


class LogoutView(RedirectView):
    '''
    GET: close a user session, clean permissions and redirect to
    login
    '''
    def get(self, request, *args, **kwargs):
        try:
            logout(request)
            del request.session['user_perms']
        except:
            pass
        return redirect(reverse('accounts:login'))
