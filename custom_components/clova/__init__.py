"""Support for CEK on CLOVA Home extension."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

from .schema import CLOVA_SCHEMA
from .http import ClovaView, ClovaConfig

_LOGGER = logging.getLogger(__name__)


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