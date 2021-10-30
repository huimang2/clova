"""Support for CEK on CLOVA Home extension."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_ENTITY_CONFIG,
    CONF_EXPOSE,
    CONF_EXPOSE_BY_DEFAULT,
    CONF_EXPOSED_DOMAINS,
    CONF_LOCATION,
    DEFAULT_EXPOSE_BY_DEFAULT,
    DEFAULT_EXPOSED_DOMAINS,
    DOMAIN,
)

from .http import ClovaView, ClovaConfig

_LOGGER = logging.getLogger(__name__)


ENTITY_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_EXPOSE, default=True): cv.boolean,
        vol.Optional(CONF_LOCATION): cv.string,
    }
)

CLOVA_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_EXPOSE_BY_DEFAULT, default=DEFAULT_EXPOSE_BY_DEFAULT
        ): cv.boolean,
        vol.Optional(
            CONF_EXPOSED_DOMAINS, default=DEFAULT_EXPOSED_DOMAINS
        ): cv.ensure_list,
        vol.Optional(CONF_ENTITY_CONFIG): {cv.entity_id: ENTITY_SCHEMA},
    }
)

CONFIG_SCHEMA = vol.Schema(
    {vol.Optional(DOMAIN): CLOVA_SCHEMA}, extra=vol.ALLOW_EXTRA
)

async def async_setup(hass: HomeAssistant, yaml_config: ConfigType) -> bool:

    if DOMAIN not in yaml_config:
        return True

    config = yaml_config[DOMAIN]
    clova_config = ClovaConfig(hass, config)

    hass.http.register_view(ClovaView(clova_config))

    return True