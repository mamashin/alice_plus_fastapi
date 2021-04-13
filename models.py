# -*- coding: utf-8 -*-

__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'
from fastapi import Form
from pydantic import BaseModel
from typing import List, Set, Optional
from redis import StrictRedis
from decouple import config

redis = StrictRedis(host=config('REDIS_SRV'), port=6379, db=0, decode_responses=True)


def form_body(cls):
    """ From body form url to json helper """
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
class GetTokenModel(BaseModel):
    code: str
    client_secret: str
    grant_type: str
    client_id: str


class DeviceModel(BaseModel):
    id: str
    capabilities: List[Optional[dict]] = None
    custom_data: Optional[dict] = None


class ListDevicesModel(BaseModel):
    devices: List[DeviceModel]


class PayloadListDevicesModel(BaseModel):
    payload: ListDevicesModel
