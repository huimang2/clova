"""Support for CEK on CLOVA Home extension."""
from __future__ import annotations

import logging
import voluptuous as vol

from typing import Any
from collections import OrderedDict

from homeassistant.const import (
    CONF_NAME,
    ATTR_DEVICE_CLASS,
    ATTR_CONNECTIONS,
    CONF_ENTITY_ID,
)
from homeassistant.core import HomeAssistant
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType, Any
from homeassistant.helpers.template import Template
from homeassistant.components import websocket_api
from homeassistant.components.websocket_api import ActiveConnection, event_message
from homeassistant.config_entries import ConfigEntry

from .const import (
    ATTR_CONFIG,
    CONF_EXPOSE,
    CONF_IR,
    CONF_ENTITY_CONFIG,
    CONF_KEY,
    CONF_MANUFACTURER,
    CONF_MODEL,
    CONF_VERSION,
    CONF_DESCRIPTION,
    CONF_LOCATION,
    CONF_TYPE,
    CONF_VALUE,
    CONF_ENTRY,
    DATA_EXTRA_MODULE_URL,
    DOMAIN,
    ICON,
    LOCATION,
    PATH_BASE,
    PATH_JS,
    PATH_JS_FILE,
    PATH_PANEL,
    SIDEBAR_TITLE,
)

from .schema import CLOVA_SCHEMA
from .http import ClovaView, ClovaConfig
from .helpers import _get_registry_entries, get_clova_type

_LOGGER = logging.getLogger(__name__)


CONFIG_SCHEMA = vol.Schema(
    {vol.Optional(DOMAIN): CLOVA_SCHEMA}, extra=vol.ALLOW_EXTRA
)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:

    hass.data.setdefault(DOMAIN, {ATTR_CONFIG:{}, ATTR_CONNECTIONS:[]})

    if DOMAIN in config:
        hass.data[DOMAIN][ATTR_CONFIG] = orderd_dict_to_dict(config[DOMAIN])

    # 웹소켓 설정
    websocket_api.async_register_command(hass, websocket_connect)
    websocket_api.async_register_command(hass, websocket_update)

    # js 파일 경로 설정
    hass.http.register_static_path(PATH_BASE, PATH_JS.format(hass.config.config_dir), cache_headers=False)

    # js 파일 추가
    if DATA_EXTRA_MODULE_URL not in hass.data:
        hass.data[DATA_EXTRA_MODULE_URL] = set()

    hass.data[DATA_EXTRA_MODULE_URL].add(PATH_JS_FILE)

    # entry 추가
    if not (entries := hass.config_entries.async_entries(DOMAIN)):
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": config_entries.SOURCE_IMPORT},
                data=hass.data[DOMAIN][ATTR_CONFIG]
            )
        )
    else:
        hass.data[DOMAIN][ATTR_CONFIG].update(entries[0].data)

    # config 설정
    clova_config = ClovaConfig(hass)

    # 패널 설정
    if DOMAIN not in hass.data.get("frontend_panels", {}):
        hass.components.frontend.async_register_built_in_panel(
            component_name="custom",
            sidebar_title=SIDEBAR_TITLE,
            sidebar_icon=ICON,
            frontend_url_path=DOMAIN,
            config={
                "_panel_custom": {
                    "name": "clova-panel",
                    "embed_iframe": False,
                    "trust_external": False,
                    "module_url": PATH_PANEL,
                },
            },
            require_admin=True,
        )

    hass.http.register_view(ClovaView(clova_config))

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CLOVA Home extension from a config entry."""
    hass.config_entries.async_update_entry(
        entry, data={}
    )
    hass.config_entries.async_update_entry(
        entry, data=hass.data[DOMAIN][ATTR_CONFIG]
    )
    hass.data[DOMAIN][CONF_ENTRY] = entry

    return True


def orderd_dict_to_dict(value: Any)-> Any:
    """ orderdDict를 dict로 변환 """

    if isinstance(value, list):
        return_list = value.copy()
        for idx, element in enumerate(return_list):
            return_list[idx] = orderd_dict_to_dict(element)
        return return_list

    elif isinstance(value, dict) or isinstance(value, OrderedDict):
        return {
            orderd_dict_to_dict(key): orderd_dict_to_dict(element)
            for key, element in value.items()
        }

    elif isinstance(value, Template):
        return value.template

    else:
        return value

    return value


@websocket_api.require_admin
@websocket_api.async_response
@websocket_api.websocket_command(
    {
        vol.Required(CONF_TYPE): "clova/connect",
    }
)
async def websocket_connect(
    hass: HomeAssistant, connection: ActiveConnection, msg: dict
) -> None:

    connections = hass.data[DOMAIN][ATTR_CONNECTIONS]

    def disconnect():
        connections.remove((connection, msg["id"]))

    connection.subscriptions[msg["id"]] = disconnect
    connections.append((connection, msg["id"]))

    default_config = {}
    config = hass.data[DOMAIN][ATTR_CONFIG]

    for state in hass.states.async_all():
        device_entry, area_entry = _get_registry_entries(hass, state.entity_id)
        entity_config = config.get(CONF_ENTITY_CONFIG,{}).get(state.entity_id, {})

        default_config[state.entity_id] = {
            CONF_MANUFACTURER: device_entry.manufacturer if device_entry else '',
            CONF_MODEL: device_entry.model if device_entry else '',
            CONF_VERSION: device_entry.sw_version if device_entry else '',
            CONF_LOCATION: LOCATION.get(area_entry.name, '') if area_entry and area_entry.name else '',
            CONF_TYPE: get_clova_type(state.domain, state.attributes.get(ATTR_DEVICE_CLASS)),
        }

    connection.send_message(
        event_message(
            msg["id"],
            {
                "id": msg["id"],
                "command": "connect",
                "data":
                {
                    "default_config": default_config,
                    "clova_config": orderd_dict_to_dict(hass.data[DOMAIN][ATTR_CONFIG])
                }
            }
        )
    )


@websocket_api.require_admin
@websocket_api.async_response
@websocket_api.websocket_command(
    {
        vol.Required(CONF_TYPE): "clova/update",
        vol.Required(CONF_ENTITY_ID): cv.entity_id,
        vol.Required(CONF_KEY): cv.string,
        vol.Required(CONF_VALUE): vol.Any(int, cv.boolean, cv.string, dict, list)
    }
)
async def websocket_update(
    hass: HomeAssistant, connection: ActiveConnection, msg: dict
) -> None:
    if msg[CONF_KEY] in [
        CONF_EXPOSE,
        CONF_NAME,
        CONF_TYPE,
        CONF_IR,
        CONF_MODEL,
        CONF_VERSION,
        CONF_DESCRIPTION
    ]:
        if msg[CONF_VALUE] or msg[CONF_KEY] in [CONF_IR, CONF_EXPOSE] :
            hass.data[DOMAIN][ATTR_CONFIG][CONF_ENTITY_CONFIG][msg[CONF_ENTITY_ID]].update({
                msg[CONF_KEY]: msg[CONF_VALUE]
            })
        else:
            del hass.data[DOMAIN][ATTR_CONFIG][CONF_ENTITY_CONFIG][msg[CONF_ENTITY_ID]][msg[CONF_KEY]]

    hass.config_entries.async_update_entry(
        hass.data[DOMAIN][CONF_ENTRY], data={}
    )
    hass.config_entries.async_update_entry(
        hass.data[DOMAIN][CONF_ENTRY], data=orderd_dict_to_dict(hass.data[DOMAIN][ATTR_CONFIG])
    )

    connections = hass.data[DOMAIN][ATTR_CONNECTIONS]

    for _connection in connections:
        _connection[0].send_message(
            event_message(
                _connection[1],
                {
                    "id": _connection[1],
                    "command": "update",
                    "data" : {
                        "clova_config": orderd_dict_to_dict(hass.data[DOMAIN][ATTR_CONFIG])
                    }
                }
            )
        )
