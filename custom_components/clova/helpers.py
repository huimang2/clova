"""CLOVA Home extension 도우미 클래스"""
from __future__ import annotations

from abc import ABC, abstractmethod
from asyncio import gather
from typing import Any
import logging
import re

from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_SUPPORTED_FEATURES,
    CONF_SERVICE,
    CONF_SERVICE_DATA,
    CLOUD_NEVER_EXPOSED_ENTITIES,
    CONF_NAME,
)
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers.area_registry import AreaEntry
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.entity_registry import RegistryEntry
from homeassistant.helpers import template

from .action import ACTIONS
from .const import (
    ACTIONS as _ACTIONS,
    ATTR_ACTION,
    ATTR_ACTIONS,
    ATTR_ACTION_DETAILS,
    ATTR_ADDITIONAL_APPLIANCE_DETAILS,
    ATTR_ALLOWABLE_VALUE,
    ATTR_APPLIANCE_ID,
    ATTR_APPLIANCE_TYPES,
    ATTR_DATA,
    ATTR_FRIENDLY_NAME,
    ATTR_FRIENDLY_DESCRIPTION,
    ATTR_HEADER,
    ATTR_IS_IR,
    ATTR_LOCATION,
    ATTR_MANUFACTURE_NAME,
    ATTR_MESSAGE_ID,
    ATTR_MODEL_NAME,
    ATTR_NAME,
    ATTR_NAMESPACE,
    ATTR_PAYLOAD_VERSION,
    ATTR_SERVICE,
    ATTR_TAGS,
    ATTR_VERSION,
    INTERFACE_GET,
    PREFIX_GET,
    SUFFIX_REQUEST,
    SUFFIX_RESPONSE,
    SUFFIX_CONFIRMATION,
    LOCATION,
    CONF_ACTION,
    CONF_ACTION_DETAILS,
    CONF_ALLOWABLE_VALUE,
    CONF_LOCATION,
    CONF_MANUFACTURER,
    CONF_MODEL,
    CONF_VERSION,
    CONF_DESCRIPTION,
    CONF_IR,
    CONF_TYPE,
    CONF_TAGS,
    CONF_RESPONSE,
    DEVICE_CLASS_TO_CLOVA_TYPES,
    DOMAIN,
    DOMAIN_TO_CLOVA_TYPES,
    ERR_UNSUPPORTED_OPERATION_ERROR,
    ERR_VALUE_NOT_SUPPORTED_ERROR,
    ERR_DRIVER_INTERNAL_ERROR,
    ERR_NO_SUCH_TARGET_ERROR
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

    @property
    def custom_commands(self):
        """ 커스텀 명령어 반환 """
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
        """ 디바이스 조회 응답(Response) 메시지 직렬화 """

        state = self.state
        
        entity_config = self.config.entity_config.get(state.entity_id, {})
        name = (entity_config.get(CONF_NAME) or state.name).strip()
        domain = state.domain
        device_class = state.attributes.get(ATTR_DEVICE_CLASS)
        entity_entry, device_entry = await _get_entity_and_device(
            self.hass, state.entity_id
        )

        actions = self.actions()
        device_type = entity_config.get(CONF_TYPE) or get_clova_type(domain, device_class)

        if not device_type:
            raise Exception(ERR_NO_SUCH_TARGET_ERROR)

        action_details = {
            ATTR_ACTION_DETAILS: [
                {
                    ATTR_ACTION: k,
                    ATTR_ALLOWABLE_VALUE: v[CONF_ALLOWABLE_VALUE]
                }
                for k, v in entity_config.get(CONF_ACTION_DETAILS, {}).items()
                if CONF_ALLOWABLE_VALUE in v
            ]
        }

        device = {
            ATTR_APPLIANCE_ID: state.entity_id,
            ATTR_FRIENDLY_NAME: name ,
            ATTR_IS_IR : entity_config.get(CONF_IR),
            ATTR_ACTIONS: list(set(action.name for action in actions) | set(action for action in entity_config.get(ATTR_ACTION_DETAILS, {}))),
            ATTR_APPLIANCE_TYPES: [device_type.upper()],
            ATTR_ADDITIONAL_APPLIANCE_DETAILS: action_details if action_details.get(ATTR_ACTION_DETAILS) else  {}
        }
        
        if device_entry:
            device.update( {
                ATTR_MANUFACTURE_NAME: device_entry.manufacturer,
                ATTR_MODEL_NAME: device_entry.model,
                ATTR_VERSION: device_entry.sw_version
            })

        if location := entity_config.get(CONF_LOCATION):
            device[ATTR_LOCATION] = location
        else:
            area = await _get_area(self.hass, entity_entry, device_entry)
            if area and area.name:
                if LOCATION.get(area.name):
                    device[ATTR_LOCATION] = LOCATION.get(area.name)
                else:
                    device[ATTR_TAGS] = [area.name]

        if description := entity_config.get(CONF_DESCRIPTION):
            device[ATTR_FRIENDLY_DESCRIPTION] = description

        if manufacturer :=  entity_config.get(CONF_MANUFACTURER):
            device[ATTR_MANUFACTURE_NAME] = manufacturer

        if model :=  entity_config.get(CONF_MODEL):
            device[ATTR_MODEL_NAME] = model

        if version :=  entity_config.get(CONF_VERSION):
            device[ATTR_VERSION] = version

        if tags := entity_config.get(CONF_TAGS):
            device[ATTR_TAGS] = tags

        return device


    def service_data_replace(self, value: Any, params:dict) -> Any:
        """ 응답 데이터 변환 """

        if isinstance(value, list):
            return_list = value.copy()
            for idx, element in enumerate(return_list):
                return_list[idx] = self.service_data_replace(element, params)
            return return_list

        if isinstance(value, dict):
            return {
                self.service_data_replace(key, params): self.service_data_replace(element, params)
                for key, element in value.items()
            }

        if isinstance(value, str):
            
            for _ in set(re.findall(r"@([\w\.]+)@", value)):
                __ = params.copy()
                for ___ in _.split("."):
                    if __ := __.get(___):
                        continue
                    else: break
                if __:
                    value = value.replace(f"@{_}@", str(__))
                
            return value

        return value


    async def execute(self, data, payload):
        """ 요청(Request)에 대한 액션 수행 """

        _action = payload["action"]
        params = payload.get("params", {})
        executed = False

        # 액션에 세부사항이 있는지 확인
        entity_config = self.config.entity_config.get(self.state.entity_id, {})
        action_detail = entity_config.get(CONF_ACTION_DETAILS, {}).get(_action, {})

        # 템플릿 적용

        try:
            template.attach(self.hass, action_detail)
            action_detail = template.render_complex(action_detail)
        except:
            raise Exception(ERR_DRIVER_INTERNAL_ERROR)

        response = self.service_data_replace(action_detail.get(CONF_RESPONSE, {}), params)

        # 서비스가 있으면 서비스를 실행하고 응답(Response) 메시지 반환
        if service := action_detail.get(CONF_SERVICE):

            domain, service = service.split(".", 1)
            service_data = self.service_data_replace(action_detail.get(CONF_SERVICE_DATA, {}), params)

            await self.hass.services.async_call(
                domain,
                service,
                service_data,
                blocking=True,
            )

        # 서비스와 응답 메시지가 없으면 기본 액션을 실행하고 응답 메시지 반환
        elif not response:
            for action in self.actions():
                if action.can_execute(_action, params):
                    response = await action.execute(data, params)
                    executed = True
                    break

            if not executed:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

        return response

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