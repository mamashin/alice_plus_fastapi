# -*- coding: utf-8 -*-

__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from fastapi import Depends, FastAPI, HTTPException, status, Request, Header
from fastapi.responses import Response, RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from models import GetTokenModel, PayloadListDevicesModel, ListDevicesModel
from services import all_device_list, device_query, device_action
from fake_yandex_oauth import fake_yandex_oauth
from decouple import config
from loguru import logger
from pathlib import Path

BASE_PATH = Path(__file__).resolve(strict=True).parent
print(BASE_PATH)
logger.add(f"{BASE_PATH}/logs/main.log", rotation="32 MB")

app = FastAPI()
app.debug = True


def access_deny():
    return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


oauth2_scheme_code = OAuth2AuthorizationCodeBearer(tokenUrl="token", authorizationUrl="auth")


async def check_auth(token: str = Depends(oauth2_scheme_code)):
    if token != fake_yandex_oauth['token']:
        raise access_deny()
    return True


@app.head("/yandex/v1.0")
async def return_ok():
    return Response(status_code=200)


@app.get("/yandex/v1.0/user/devices")
async def get_devices_list(x_request_id: str = Header(None), auth_ok: bool = Depends(check_auth)):
    reply = all_device_list(x_request_id)
    logger.debug(reply)
    return reply


@app.post("/yandex/v1.0/user/devices/action")
async def yandex_action(device_list: PayloadListDevicesModel,
                        x_request_id: str = Header(None),
                        auth_ok: bool = Depends(check_auth)):
    logger.debug(device_list)
    return device_action(x_request_id, device_list)


@app.post("/yandex/v1.0/user/devices/query")
async def yandex_query(dev_list: ListDevicesModel,
                       x_request_id: str = Header(None),
                       auth_ok: bool = Depends(check_auth)):
    logger.debug(dev_list)
    return device_query(x_request_id, dev_list)


@app.get("/auth/enter/")
async def auth_enter(client_id: str, response_type: str, redirect_uri: str, state: str):
    if client_id != fake_yandex_oauth['client_id']:
        raise access_deny()
    redirect = f'{state}/?code={fake_yandex_oauth["client_code"]}'
    return RedirectResponse(redirect)


@app.post("/auth/token/")
async def auth_token(request_model=Depends(GetTokenModel)):
    if request_model.code != fake_yandex_oauth['client_code'] or \
            request_model.client_secret != fake_yandex_oauth['client_secret']:
        raise access_deny()
    return {"access_token": fake_yandex_oauth['token'], "token_type": "bearer"}


@app.post("/yandex/v1.0/user/unlink")
async def yandex_unlink(auth_ok: bool = Depends(check_auth)):
    return Response(status_code=200)
