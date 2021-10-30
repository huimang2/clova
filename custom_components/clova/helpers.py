"""CLOVA Home extension 도우미 클래스"""
from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import gather
import logging

from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_SUPPORTED_FEATURES,
    CLOUD_NEVER_EXPOSED_ENTITIES,
    CONF_NAME,
)
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers.area_registry import AreaEntry
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.entity_registry import RegistryEntry

from .action import ACTIONS
from .const import (
    ACTIONS as _ACTIONS,
    ATTR_ACTIONS,
    ATTR_ADDITIONAL_APPLIANCE_DETAILS,
    ATTR_APPLIANCE_ID,
    ATTR_APPLIANCE_TYPES,
    ATTR_FRIENDLY_NAME,
    ATTR_HEADER,
    ATTR_IS_IR,
    ATTR_LOCATION,
    ATTR_MANUFACTURE_NAME,
    ATTR_MESSAGE_ID,
    ATTR_MODEL_NAME,
    ATTR_NAME,
    ATTR_NAMESPACE,
    ATTR_PAYLOAD_VERSION,
    ATTR_VERSION,
    INTERFACE_GET,
    PREFIX_GET,
    SUFFIX_REQUEST,
    SUFFIX_RESPONSE,
    SUFFIX_CONFIRMATION,
    LOCATION,
    CONF_LOCATION,
    DEVICE_CLASS_TO_CLOVA_TYPES,
    DOMAIN,
    DOMAIN_TO_CLOVA_TYPES,
    ERR_VALUE_NOT_SUPPORTED_ERROR
)

_LOGGER = logging.getLogger(__name__)


async def _get_entity_and_device(
    hass, entity_id
) -> tuple[RegistryEntry, DeviceEntry] | None:
    """entity_id에 대한 entity와 device entry를 가져옴"""
    dev_reg, ent_reg = await gather(
        hass.helpers.device_registry.async_get_registry(),
        hass.helpers.entity_registry.async_get_registry(),
    )

    if not (entity_entry := ent_reg.async_get(entity_id)):
        return None, None
    device_entry = dev_reg.devices.get(entity_entry.device_id)
    return entity_entry, device_entry


async def _get_area(hass, entity_entry, device_entry) -> AreaEntry | None:
    """ entity에 대한 장소 계산 """
    if entity_entry and entity_entry.area_id:
        area_id = entity_entry.area_id
    elif device_entry and device_entry.area_id:
        area_id = device_entry.area_id
    else:
        return None

    area_reg = await hass.helpers.area_registry.async_get_registry()
    return area_reg.areas.get(area_id)


class AbstractConfig(ABC):
    """ CLOVA Home extension 설정 베이스 """

    def __init__(self, hass):
        """ 추상 클래스 초기화 """
        self.hass = hass

    @property
    def entity_config(self):
        """ entity config 반환 """
        return {}

    @abstractmethod
    def should_expose(self, state) -> bool:
        """ 노출되어야 하는지를 설정 """


class RequestData:
    """요청과 관련된 데이터 고정"""

    def __init__(
        self,
        config: AbstractConfig,
        message: dict,
    ) -> None:
        """Initialize the request data."""
        self.messageId = message[ATTR_HEADER][ATTR_MESSAGE_ID]
        self.name = message[ATTR_HEADER][ATTR_NAME]
        self.namespace = message[ATTR_HEADER][ATTR_NAMESPACE]
        self.payloadVersion = message[ATTR_HEADER][ATTR_PAYLOAD_VERSION]
        self.config = config
        self.action = self.name.replace(SUFFIX_REQUEST, "")
        self.response = _ACTIONS[self.action].response
        self.prefix = _ACTIONS[self.action].prefix
        self.suffix = _ACTIONS[self.action].suffix
        self.domain = _ACTIONS[self.action].domain


def get_clova_type(domain, device_class):
    """ 도메인(domain)과 기기 클레스(device class)에 따른 CLOVA 타입 설정 """
    typ = DEVICE_CLASS_TO_CLOVA_TYPES.get((domain, device_class))
    
    return typ if typ is not None else DOMAIN_TO_CLOVA_TYPES.get(domain)


class ClovaEntity:
    """ CLOVA 구성요소 추상화 클래스 """
    
    def __init__(
        self, hass: HomeAssistant, config: AbstractConfig, state: State
    ) -> None:
        """ CLOVA 구성요소 초기화 """
        self.hass = hass
        self.config = config
        self.state = state
        self._actions = None

    @property
    def entity_id(self):
        """ entity ID 반환 """
        return self.state.entity_id

    @callback
    def actions(self):
        """ 구성요소가 사용가능한 액션 반환 """
        if self._actions is not None:
            return self._actions

        state = self.state
        domain = state.domain
        attributes = state.attributes
        features = attributes.get(ATTR_SUPPORTED_FEATURES, 0)

        if not isinstance(features, int):
            _LOGGER.warning(
                "Entity %s contains invalid supported_features value %s",
                self.entity_id,
                features,
            )
            return []

        device_class = state.attributes.get(ATTR_DEVICE_CLASS)

        self._actions = [
            action(self.hass, state, self.config)
            for action in ACTIONS
            if action.supported(domain, features, device_class, attributes)
        ]
        return self._actions

    @callback
    def should_expose(self):
        """ 구성요소의 노출 여부 반환 """
        return self.config.should_expose(self.state)


    async def sync_serialize(self):
        """ 응답(Response) 메시지 직렬화 """

        state = self.state

        entity_config = self.config.entity_config.get(state.entity_id, {})
        name = (entity_config.get(CONF_NAME) or state.name).strip()
        domain = state.domain
        device_class = state.attributes.get(ATTR_DEVICE_CLASS)
        entity_entry, device_entry = await _get_entity_and_device(
            self.hass, state.entity_id
        )

        actions = self.actions()

        device_type = get_clova_type(domain, device_class)

        device = {
            ATTR_APPLIANCE_ID: state.entity_id,
            ATTR_FRIENDLY_NAME: name ,
            ATTR_IS_IR : False,
            ATTR_ACTIONS: [action.name for action in actions],
            ATTR_APPLIANCE_TYPES: [device_type],
            ATTR_ADDITIONAL_APPLIANCE_DETAILS: {}
        }
        
        if device_entry:
            device.update( {
                ATTR_MANUFACTURE_NAME: device_entry.manufacturer,
                ATTR_MODEL_NAME: device_entry.model,
                ATTR_VERSION: device_entry.sw_version
            })

        for action in actions:
            device[ATTR_ADDITIONAL_APPLIANCE_DETAILS].update(action.sync_attributes())

        if location := entity_config.get(CONF_LOCATION):
            device[ATTR_LOCATION] = LOCATION.get(location, location)
        else:
            area = await _get_area(self.hass, entity_entry, device_entry)
            if area and area.name:
                device[ATTR_LOCATION] = LOCATION.get(area.name,area.name)

        return device

    async def execute(self, data, payload):
        """ 요청(Request)에 대한 액션 수행 """
        _action = payload["action"]
        params = payload.get("params", {})
        executed = False
        
        for action in self.actions():
            if action.can_execute(_action, params):
                result = await action.execute(data, params)
                executed = True
                break

        if not executed:
            raise Exception(ERR_VALUE_NOT_SUPPORTED_ERROR)

        return result

    @callback
    def async_update(self):
        """ Home Assistant의 최신 상태로 구성요소 업데이트 """
        self.state = self.hass.states.get(self.entity_id)

        if self._actions is None:
            return

        for action in self._actions:
            action.state = self.state

@callback
def async_get_entities(hass, config) -> list:
    """ CLOVA에 의해 지원되는 모든 구성요소 반환 """
    entities = []
    for state in hass.states.async_all():
        if state.entity_id in CLOUD_NEVER_EXPOSED_ENTITIES:
            continue

        entity = ClovaEntity(hass, config, state)
        entities.append(entity)

    return entities