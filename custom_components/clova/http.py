""" CLOVA Home extension - HTTP 처리 """
from __future__ import annotations

import logging
import base64

from aiohttp.web import Request, Response
from homeassistant.components.http import HomeAssistantView
from homeassistant.const import (
    CLOUD_NEVER_EXPOSED_ENTITIES,
)
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

from .const import (
    CONF_ENTITY_CONFIG,
    CONF_EXPOSE,
    CONF_EXPOSE_BY_DEFAULT,
    CONF_EXPOSED_DOMAINS,
    ATTR_ACCESS_TOKEN,
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


class ClovaConfig(AbstractConfig):
    """ CLOVA Home extension 수동 설정 """

    def __init__(self, hass, config):
        """Initialize the config."""
        super().__init__(hass)
        self._config = config

    @property
    def entity_config(self):
        """Return entity config."""
        return self._config.get(CONF_ENTITY_CONFIG) or {}

    def should_expose(self, state) -> bool:
        """Return if entity should be exposed."""
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

    async def post(self, request: Request) -> Response:

        message: dict = await request.json()
        signature_base64: string = request.headers[ATTR_SIGNATURECEK]
        signature: bytes = base64.b64decode(request.headers[ATTR_SIGNATURECEK])

        del message[ATTR_PAYLOAD][ATTR_ACCESS_TOKEN]
        
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

        """ 요청 메시지 처리 """
        response = await async_handle_message(
            request.app["hass"], 
            self.config, 
            message
        )

        return self.json(response)
