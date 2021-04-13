# -*- coding: utf-8 -*-

__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'


def devs():
    return [
        {
            "id": "c069dc6b",
            "name": "Основной свет",
            "description": "Основной свет на кухне",
            "room": "Кухня",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                }
            ],
            "mqtt": {
                "get": "kitchen/light/main/ro",
                "set": "kitchen/light/main/rw",
            }
        },

        {
            "id": "3bd5f02b",
            "name": "Свет над столом",
            "description": "Торшер на кухне над столом",
            "room": "Кухня",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                }
            ],
            "mqtt": {
                "get": "kitchen/light/table/ro",
                "set": "kitchen/light/table/rw",
            }
        },

        {
            "id": "40daf02c",
            "name": "Свет в ванне",
            "description": "Основной свет в ванне",
            "room": "Ванна",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                }
            ],
            "mqtt": {
                "get": "bathroom/light/main/ro",
                "set": "bathroom/light/main/rw",
            }
        },

        {
            "id": "93da70ec",
            "name": "Подсветка в ванне",
            "description": "Подсветка в ванне",
            "room": "Ванна",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                }
            ],
            "mqtt": {
                "get": "bathroom/light/mirror/ro",
                "set": "bathroom/light/mirror/rw",
            }
        },

        {
            "id": "2c2afdbd",
            "name": "Первый свет в спальне",
            "description": "Первый свет в спальне",
            "room": "Спальня",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                }
            ],
            "mqtt": {
                "get": "bad_room/light/roof_1/ro",
                "set": "bad_room/light/roof_1/rw",
            }
        },

        {
            "id": "c5dabb15",
            "name": "Второй свет в спальне",
            "description": "Второй свет в спальне",
            "room": "Спальня",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                }
            ],
            "mqtt": {
                "get": "bad_room/light/roof_2/ro",
                "set": "bad_room/light/roof_2/rw",
            }
        },

        {
            "id": "edad3f03",
            "name": "Первый свет в детской",
            "description": "Первый свет в детской",
            "room": "Детская",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                }
            ],
            "mqtt": {
                "get": "children/light/roof_1/ro",
                "set": "children/light/roof_1/rw",
            }
        },

        {
            "id": "51a032dd",
            "name": "Второй свет в детской",
            "description": "Второй свет в детской",
            "room": "Детская",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                }
            ],
            "mqtt": {
                "get": "children/light/roof_2/ro",
                "set": "children/light/roof_2/rw",
            }
        },

        {
            "id": "a7a9c1d1",
            "name": "Датчик влажности",
            "description": "Датчик влажности",
            "room": "Ванна",
            "type": "devices.types.sensor",
            "capabilities": [],
            "properties": [{
                "type": "devices.properties.float",
                "retrievable": True,
                "reportable": True,
                "parameters": {
                    "instance": "humidity",
                    "unit": "unit.percent"
                }
            }],
            "mqtt": {
                "get": "bathroom/humidity/ro"
            }
        },

        {
            "id": "e5fcb115",
            "name": "Датчик температуры",
            "description": "Датчик температуры",
            "room": "Ванна",
            "type": "devices.types.sensor",
            "capabilities": [],
            "properties": [{
                "type": "devices.properties.float",
                "retrievable": True,
                "reportable": True,
                "parameters": {
                    "instance": "temperature",
                    "unit": "unit.temperature.celsius"
                }
            }],
            "mqtt": {
                "get": "bathroom/temp/ro"
            }
        },

        {
            "id": "15fab355",
            "name": "Датчик температуры",
            "description": "Датчик температуры",
            "room": "Спальня",
            "type": "devices.types.sensor",
            "capabilities": [],
            "properties": [{
                "type": "devices.properties.float",
                "retrievable": True,
                "reportable": True,
                "parameters": {
                    "instance": "temperature",
                    "unit": "unit.temperature.celsius"
                }
            }],
            "mqtt": {
                "get": "bad_room/temp/ro"
            }
        },

        {
            "id": "95feb102",
            "name": "Лента",
            "description": "Светодиодная лента на балконе",
            "room": "Балкон",
            "type": "devices.types.light",
            "capabilities": [
                {
                    "type": "devices.capabilities.on_off",
                    "retrievable": True,
                    "state": {"instance": "on", "value": False}
                },
                {
                    "type": "devices.capabilities.color_setting",
                    "retrievable": True,
                    "reportable": False,
                    "parameters": {
                        "color_model": "rgb"
                    },
                    "state": {"instance": "rgb", "value": 0}
                },
                {
                    "type": "devices.capabilities.range",
                    "retrievable": True,
                    "reportable": False,
                    "parameters": {
                        "instance": "brightness",
                        "random_access": True,
                        "range": {
                            "max": 100,
                            "min": 0,
                            "precision": 1
                        },
                        "unit": "unit.percent"
                    },
                    "state": {"instance": "brightness", "value": 0}
                }
            ],
            "mqtt": {
                "get": "balkon/light/rgb/ro",
                "set": "balkon/light/rgb/rw",
            },
            "custom_type": "rgb_light"
        }
    ]
