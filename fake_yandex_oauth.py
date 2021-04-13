# -*- coding: utf-8 -*-

__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from decouple import config


fake_yandex_oauth = {
    "client_id": config('CLIENT_ID'),
    "client_secret": config('CLIENT_SECRET'),
    "client_code": config('CLIENT_CODE'),
    "token": config('TOKEN'),
    "user_id": config('USER_ID')
}
