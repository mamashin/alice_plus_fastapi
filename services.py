# -*- coding: utf-8 -*-

__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from devices import devs
from utils import dictor
from fake_yandex_oauth import fake_yandex_oauth
from models import ListDevicesModel, PayloadListDevicesModel, redis
import paho.mqtt.publish as mqtt
from decouple import config
from loguru import logger
from pathlib import Path

BASE_PATH = Path(__file__).resolve(strict=True).parent
logger.add(f"{BASE_PATH}/logs/services.log", rotation="32 MB")


def base_yandex_reply(request_id):
    """ Базовый ответ на запросы со стороны Яндекса"""
    return {
        "request_id": request_id,
        "payload": {
            "user_id": fake_yandex_oauth["user_id"],
            "devices": []
        }
    }


def dev2yandex(dev):
    """ Преобразуем базу наших устройств в формат понятный Яндексу"""
    return {
        "id": dictor(dev, "id", ""),
        "name": dictor(dev, "name", "Без названия"),
        "room": dictor(dev, "room", ""),
        "description": dictor(dev, "description", ""),
        "type": dictor(dev, "type", "devices.types.light"),
        "custom_data": {
            "mqtt": dictor(dev, "mqtt", {}),
            "type": dictor(dev, "custom_type", {}),
        },
        "capabilities": dictor(dev, "capabilities", [
            {
                "type": "devices.capabilities.on_off",
                "retrievable": True,
                "state": {"instance": "on", "value": False}
            }
        ]),
        "properties": dictor(dev, "properties", [])
    }


def mqtt_send(topic, value):
    """ Отправляем данные в MQTT """
    try:
        mqtt.single(topic=topic, payload=value, hostname=config('MQTT_SRV'),
                    port=1883, client_id="alice_to_mqtt", qos=0)
    except Exception as e:
        logger.exception(e)
        return False
    return True


def all_device_list(request_id):
    """ Отдаем Яндексу список всех наших устройств"""
    reply = base_yandex_reply(request_id)
    for dev in devs():
        reply["payload"]["devices"].append(dev2yandex(dev))
    return reply


def device_query(request_id: str, device_list: ListDevicesModel):
    """ Отдаем текущий статус устройства """
    reply = base_yandex_reply(request_id)
    for dev_query in device_list.devices:
        if my_device := next((item for item in devs() if item.get("id") and item["id"] == dev_query.id), False):
            """ Ищем в нашей базе устройство которе запросил Яндекс и если оно есть - отдаем статус"""
            return_cap = []
            for dev_cap in my_device["capabilities"]:
                if dev_cap["type"] == "devices.capabilities.on_off" and \
                        dictor(dev_query.custom_data, "type") != "rgb_light":
                    ret_cap = dev_cap
                    ret_cap["state"]["value"] = redis.get(my_device["mqtt"]["get"]) == "ON"
                    return_cap.append(ret_cap)
            if dictor(dev_query.custom_data, "type") == "rgb_light":
                rgb_state = eval(redis.get(my_device["mqtt"]["get"]))
                for dev_cap in my_device["capabilities"]:
                    ret_cap = dev_cap
                    ret_cap["state"]["value"] = rgb_state[dev_cap["state"]["instance"]]
                    return_cap.append(ret_cap)

            return_prop = []
            if dictor(my_device, "properties", False):
                """ Считываем информацию с датчиков"""
                for dev_prop in my_device["properties"]:
                    if dev_prop["type"] == "devices.properties.float":
                        ret_prop = dev_prop
                        dev_prop["state"] = {}
                        dev_prop["state"]["instance"] = dictor(dev_prop, "parameters.instance", "none")
                        dev_prop["state"]["value"] = float(redis.get(my_device["mqtt"]["get"]))
                        return_prop.append(ret_prop)

            if return_cap:
                my_device["capabilities"] = return_cap
            reply["payload"]["devices"].append(dev2yandex(my_device))

    return reply


def device_action(request_id: str, device_list: PayloadListDevicesModel):
    """ Отдаем текущий статус устройства """
    reply = base_yandex_reply(request_id)
    dev_state = {}
    for dev_query in device_list.payload.devices:
        if my_device := next((item for item in devs() if item.get("id") and item["id"] == dev_query.id), False):
            """ my_device - запрошенное устройство из базы найденное по id """
            dev_state = dev2yandex(my_device)
            dev_state["capabilities"] = []
            """ dev_state - в формате Яндекса """
            for dev_cap in dev_query.capabilities:
                out_cap = dev_cap
                command_status = "DONE"
                """ Если ошибка при mqtt publish или девайс не поддерживает установку состояния - 
                возвращаем ошибку"""
                if dictor(my_device, "mqtt.set") and dictor(dev_query.custom_data, "type") != "rgb_light":
                    if not mqtt_send(my_device["mqtt"]["set"], "ON" if dev_cap["state"]["value"] else "OFF"):
                        command_status = "ERROR"
                        out_cap["state"]["error_code"] = "DEVICE_UNREACHABLE"
                out_cap["state"]["action_result"] = {"status": command_status}
                dev_state['capabilities'].append(out_cap)
            if dictor(dev_query.custom_data, "type") == "rgb_light":
                mqtt_send(my_device["mqtt"]["set"], rgb_light(dev_query.capabilities))

        reply["payload"]["devices"].append(dev_state)
    logger.debug(f'Reply data: {reply}')
    return reply


def rgb_light(rgb_cap_all):
    mqtt_msg = {}
    for cap in rgb_cap_all:
        mqtt_msg[dictor(cap, "state.instance")] = dictor(cap, "state.value")
    logger.debug(f'MQTT RGB CAP: {mqtt_msg}')
    return str(mqtt_msg)  # {'on': True, 'rgb': 13303562, 'brightness': 55}

