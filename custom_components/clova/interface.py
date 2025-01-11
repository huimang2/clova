"""CLOVA Home extension - 인터페이스 처리"""
import asyncio
import logging
import re

from homeassistant.util.decorator import Registry

from .helpers import ClovaEntity, RequestData, async_get_entities
from .const import (
    ATTR_APPLIANCE,
    ATTR_APPLIANCE_ID,
    ATTR_CUSTOM_COMMANDS,
    ATTR_DISCOVERED_APPLIANCES,
    ATTR_HEADER,
    ATTR_MESSAGE_ID,
    ATTR_NAME,
    ATTR_NAMESPACE,
    ATTR_PAYLOAD,
    ATTR_PAYLOAD_VERSION,
    SUFFIX_REQUEST,
    SUFFIX_RESPONSE,
    INTERFACE_ERROR,
    INTERFACE_CONTROL,
    INTERFACE_DISCOVERY,
)

for s in INTERFACE_ERROR:
    globals()['ERR_{}'.format(re.sub(r'([A-Z])',r'_\1',s)[1:].upper())] = s

CLOVA = Registry()
_LOGGER = logging.getLogger(__name__)


async def async_handle_message(hass, config, message):
    """요청(Request) 메시지에 대한 처리"""

    data = RequestData(config, message)

    response = await _process(hass, data, message)

    if response and response[ATTR_HEADER]['name'] in INTERFACE_ERROR:
        _LOGGER.error("Error handling message %s: %s", message, response.get(ATTR_HEADER).get(ATTR_NAME))

    return response


async def _process(hass, data, message):
    """메시지 전처리"""

    if (handler := CLOVA.get(data.name)) is None:
        return sync_serialize(data, ERR_UNSUPPORTED_OPERATION_ERROR, {})

    try:
        response = await handler(hass, data, message.get(ATTR_PAYLOAD))
    except Exception as e:
        _LOGGER.error(f"ERROR: {e}")
        if e in INTERFACE_ERROR:
            return sync_serialize(data, e, message.get(ATTR_PAYLOAD))
        else:
            return sync_serialize(data, ERR_DRIVER_INTERNAL_ERROR, message.get(ATTR_PAYLOAD))

    if response is None:
        return None

    return response


def sync_serialize(data, name, payload):
    """응답(Response) 메시지 직렬화"""
    return {
        ATTR_HEADER: {
            ATTR_MESSAGE_ID: data.messageId,
            ATTR_NAME: name,
            ATTR_NAMESPACE: data.namespace,
            ATTR_PAYLOAD_VERSION: data.payloadVersion
        },
        ATTR_PAYLOAD: payload
    }


@CLOVA.register(INTERFACE_DISCOVERY)
async def DiscoverAppliancesRequest(hass, data, payload):
    """기기 조회 인터페이스 메시지 처리"""

    entities = async_get_entities(hass, data.config)
    results = await asyncio.gather(
        *(
            entity.sync_serialize()
            for entity in entities
            if entity.should_expose()
        ),
        return_exceptions=True,
    )

    devices = []

    for entity, result in zip(entities, results):
        if isinstance(result, Exception):
            _LOGGER.error("Error serializing %s", entity.entity_id, exc_info=result)
        else:
            devices.append(result)

    return sync_serialize(
        data,
        INTERFACE_DISCOVERY.replace(SUFFIX_REQUEST, SUFFIX_RESPONSE),
        {
            ATTR_CUSTOM_COMMANDS: data.config.custom_commands,
            ATTR_DISCOVERED_APPLIANCES: devices
        }
    )


async def _control_interface(hass, data, payload):
    """기기 제어 인터페이스 메시지 처리"""

    action = data.action
    entity_id = payload[ATTR_APPLIANCE][ATTR_APPLIANCE_ID]

    if (state := hass.states.get(entity_id)) is None:
        return sync_serialize(data, ERR_NO_SUCH_TARGET_ERROR, {})

    entity = ClovaEntity(hass, data.config, state)

    result = await entity.execute(data, {"action":action, "params": payload})

    return sync_serialize(data, data.response, result if result else {})


"""인터페이스 메시지 함수 생성"""
exec(''.join('''
@CLOVA.register("{}")
async def {}(hass, data, payload):
    return await _control_interface(hass, data, payload);
'''.format(__,__) for __ in INTERFACE_CONTROL))


