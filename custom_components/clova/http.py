""" CLOVA Home extension - HTTP 처리 """
from __future__ import annotations

import logging
import base64

from aiohttp.web import Request, Response
from homeassistant.components.http import HomeAssistantView
from homeassistant.const import (
    CLOUD_NEVER_EXPOSED_ENTITIES,
    CONF_ENTITY_ID,
    CONF_NAME,
)
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

from .const import (
    CONF_ACTION,
    CONF_ACTIONS,
    CONF_CUSTOM_COMMANDS,
    CONF_ENTITY_CONFIG,
    CONF_EXPOSE,
    CONF_EXPOSE_BY_DEFAULT,
    CONF_EXPOSED_DOMAINS,
    ATTR_ACCESS_TOKEN,
    ATTR_ACTION,
    ATTR_ACTIONS,
    ATTR_APPLIANCE_ID,
    ATTR_HEADER,
    ATTR_NAME,
    ATTR_PAYLOAD,
    ATTR_SIGNATURECEK,
    CLOVA_API_ENDPOINT, 
    SIGNATURE_PUBLIC_KEY,
    ERR_VALIDATION_FAILED_ERROR
)
from .helpers import AbstractConfig
from .interface import async_handle_message

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass):
    """Enable the Area Registry views."""
    _LOGGER.error("요게 되네?")
    return True


class ClovaConfig(AbstractConfig):
    """ CLOVA Home extension 수동 설정 """

    def __init__(self, hass, config):
        """ config 초기화 """
        super().__init__(hass)
        self._config = config

    @property
    def entity_config(self):
        """ entity config 리턴 """
        return self._config.get(CONF_ENTITY_CONFIG, {})

    @property
    def custom_commands(self):
        """ 사용자 커맨드 리턴 """
        return [{
            ATTR_NAME: c_cmd[CONF_NAME],
            ATTR_ACTIONS: [{
                ATTR_APPLIANCE_ID: action[CONF_ENTITY_ID],
                ATTR_ACTION: action[CONF_ACTION]
            } for action in c_cmd[CONF_ACTIONS] ]
        } for c_cmd in self._config.get(CONF_CUSTOM_COMMANDS, {}) ]

    def should_expose(self, state) -> bool:
        """ entity가 노출되어야 하는지를 설정 """
        expose_by_default = self._config.get(CONF_EXPOSE_BY_DEFAULT)
        exposed_domains = self._config.get(CONF_EXPOSED_DOMAINS)

        if state.attributes.get("view") is not None:

            return False

        if state.entity_id in CLOUD_NEVER_EXPOSED_ENTITIES:
            return False

        explicit_expose = self.entity_config.get(state.entity_id, {}).get(CONF_EXPOSE)

        domain_exposed_by_default = (
            expose_by_default and state.domain in exposed_domains
        )

        is_default_exposed = domain_exposed_by_default and explicit_expose is not False

        return is_default_exposed or explicit_expose


class ClovaView(HomeAssistantView):
    """ CEK 요청 처리 """

    url = CLOVA_API_ENDPOINT
    name = "api:clova"
    requires_auth = False # 인증키가 본문으로 전달되어 True로 하면 인증이 안됨.
                                         # 디지털 서명 검증으로 대체

    def __init__(self, config):
        """ CEK 요청 핸들러 초기화 """
        self.config = config
    
    # POST 요청
    async def post(self, request: Request) -> Response:
        _LOGGER.error(request.app["hass"])
        message: dict = await request.json()
        signature_base64: string = request.headers.get(ATTR_SIGNATURECEK)
        signature: bytes = base64.b64decode(signature_base64)
  
        # 디지털 서명 검증
        try:
            load_pem_public_key(
                SIGNATURE_PUBLIC_KEY, backend=default_backend()
            ).verify(
                signature,
                request._read_bytes,
                padding.PKCS1v15(),
                hashes.SHA256()
            )

        except Exception as e:
            _LOGGER.error("Authorization Error : ", e)
            message[ATTR_HEADER][ATTR_NAME] = ERR_VALIDATION_FAILED_ERROR

        del message[ATTR_PAYLOAD][ATTR_ACCESS_TOKEN]

        """ 요청 메시지 처리 """
        response = await async_handle_message(
            request.app["hass"], 
            self.config, 
            message
        )

        return self.json(response)