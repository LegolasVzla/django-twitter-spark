#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailBackend(ModelBackend):
    '''
    Method to authenticate user by email
    '''
    def authenticate(self, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except:
            pass
        else:
            if user.check_password(password):
                return user
        return None