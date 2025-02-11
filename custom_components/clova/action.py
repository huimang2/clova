"""CLOVA Home extension - 액션 처리"""
from __future__ import annotations

import logging
import re

from datetime import datetime

from homeassistant.components import (
    fan,
    group,
)
from homeassistant.components.climate import const as climate
from homeassistant.components.humidifier import const as humidifier
from homeassistant.components.lock import STATE_JAMMED, STATE_UNLOCKING
from homeassistant.components.media_player.const import MEDIA_TYPE_CHANNEL
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_TEMPERATURE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.core import DOMAIN as HA_DOMAIN

from .const import (
    ATTR_APPLIANCE_RESPONSE_TIMESTAMP,
    ATTR_CURRENT_TEMPERATUE,
    ATTR_DELTA_TEMPERATURE,
    ATTR_FAN_SPEED,
    ATTR_IS_TURN_ON,
    ATTR_IS_REACHABLE,
    ATTR_MODE,
    ATTR_NAME,
    ATTR_PREVIOUS_STATE,
    ATTR_STATES,
    ATTR_TARGET_TEMPERATURE,
    ATTR_UNIT,
    ATTR_VALUE,
    ACTIONS as _ACTIONS,
    HVAC_MODES,
    FAN_MODES,
    SWING_MODES,
    PRESET_MODES,
    ERR_NO_SUCH_TARGET_ERROR,
    ERR_DRIVER_INTERNAL_ERROR,
    ERR_UNSUPPORTED_OPERATION_ERROR,
    PREFIX_CHANGE,
    PREFIX_SET,
    PREFIX_GET,
    PREFIX_DECREMENT,
    PREFIX_INCREMENT,
    PREFIX_START,
    PREFIX_STOP,
    SUFFIX_ON,
    SUFFIX_OFF,
    TRANSLATION_ONDO,
    TRANSLATION_SOGDO
)

_LOGGER = logging.getLogger(__name__)


ACTIONS = []


def register_action(action):
    """Decorate a function to register action."""
    ACTIONS.append(action)
    return action


class _action:
    """CLOVA Home extension 액션"""

    def __init__(self, hass, state, config):
        """Initialize a action for a state."""
        self.hass = hass
        self.state = state
        self.config = config

    def can_execute(self, action, params):
        """Test if command can be executed."""
        return action == self.name

    async def execute(self, data, params):
        """Execute a trait command."""
        raise NotImplementedError



@register_action
class HealthCheck(_action):
    """ 상태 확인 액션 """
    name = "HealthCheck"

    @staticmethod
    def supported(domain, features, device_class, attributes):
        return domain in _ACTIONS["HealthCheck"].domain

    async def execute(self, data, params):

        if (state := self.state) is None:
            raise Exception(ERR_NO_SUCH_TARGET_ERROR)

        payload = {}
        payload[ATTR_IS_REACHABLE] = True

        if state.domain == climate.DOMAIN:
            payload[ATTR_IS_TURN_ON] = state.state in state.attributes.get(climate.ATTR_HVAC_MODES) and state.state != climate.HVACAction.OFF

        else:
            payload[ATTR_IS_TURN_ON] = state.state == STATE_ON

        return payload


@register_action
class ChangePower(_action):
    """ 전원 상태 변환 액션 """
    name = "ChangePower"

    @staticmethod
    def supported(domain, features, device_class, attributes):
        return domain in _ACTIONS["ChangePower"].domain

    async def execute(self, data, params):
        await self.hass.services.async_call(
            HA_DOMAIN
            if (service_domain := self.state.domain) == group.DOMAIN
            else service_domain,
            SERVICE_TURN_ON if self.state.state == STATE_OFF else SERVICE_TURN_ON,
            {ATTR_ENTITY_ID: self.state.entity_id},
            blocking=True,
        )


class Turn(_action):
    """ On/Off 액션 """

    async def pre_process(self, data, params):
        await self.hass.services.async_call(
            HA_DOMAIN
            if (service_domain := self.state.domain) == group.DOMAIN
            else service_domain,
            SERVICE_TURN_OFF if data.suffix == SUFFIX_OFF else SERVICE_TURN_ON,
            {ATTR_ENTITY_ID: self.state.entity_id},
            blocking=True,
        )


class Mode(_action):
    """ 모드 전환 액션 전처리"""

    async def pre_process(self, data, params):

        state = self.state

        # climate 도메인
        if state.domain == climate.DOMAIN:

            if self.state.attributes.get(climate.ATTR_HVAC_MODES) is None:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            HA_modes = [_ for _ in self.state.attributes.get(climate.ATTR_HVAC_MODES) if _ != climate.HVACAction.OFF]
            clova_modes = {y: x for x, y in HVAC_MODES.items() if y and y in HA_modes}

            current_mode = self.state.state

            # 순서 확인
            if current_mode in HA_modes:
                idx = HA_modes.index(current_mode)

            elif current_mode == climate.HVACAction.OFF:
                idx = -1

            else:
                raise Exception(ERR_DRIVER_INTERNAL_ERROR)

            # 모드 설정
            if (prefix := data.prefix) == PREFIX_CHANGE:
                next_mode = HA_modes[idx+1 if idx+1 < len(HA_modes) else 0]

            elif prefix == PREFIX_SET:
                next_mode = HVAC_MODES.get(params[ATTR_MODE][ATTR_VALUE])

                if not next_mode:
                    next_mode = HA_modes[0]

            else:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            # 액션 실행
            if next_mode != current_mode:
                await self.hass.services.async_call(
                    climate.DOMAIN,
                    climate.SERVICE_SET_HVAC_MODE,
                    {
                        ATTR_ENTITY_ID: self.state.entity_id,
                        climate.ATTR_HVAC_MODE: next_mode,
                    },
                    blocking=True,
                )

            # 응답 메시지 작성
            payload = {}

            if (prev_mode := clova_modes.get(current_mode)) and prefix == PREFIX_CHANGE :
                payload[ATTR_PREVIOUS_STATE] = {ATTR_MODE:{ATTR_VALUE:prev_mode}}

            if current_mode := clova_modes.get(next_mode):
                payload[ATTR_MODE] = {ATTR_VALUE: current_mode}


        # fan 도메인
        elif state.domain == fan.DOMAIN:

            if self.state.attributes.get(fan.ATTR_PRESET_MODES) is None:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            HA_modes = [_ for _ in self.state.attributes.get(fan.ATTR_PRESET_MODES) if _ not in ["off", None] ]
            clova_modes = {y: x for x, y in HVAC_MODES.items() if y and y in HA_modes}

            current_mode = self.state.attributes.get(fan.ATTR_PRESET_MODE)

            if data.prefix == PREFIX_SET:
                next_mode = PRESET_MODES.get(params[ATTR_MODE][ATTR_VALUE])

                if not next_mode:
                    next_mode = HA_modes[0]

            else:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            # 액션 실행
            if next_mode != current_mode:
                await self.hass.services.async_call(
                    climate.DOMAIN,
                    climate.SERVICE_SET_PRESET_MODE,
                    {
                        ATTR_ENTITY_ID: self.state.entity_id,
                        fan.ATTR_PRESET_MODE: next_mode,
                    },
                    blocking=True,
                )

            # 응답 메시지 작성
            payload = {}

            if current_mode := clova_modes.get(next_mode):
                payload[ATTR_MODE] = {ATTR_VALUE: current_mode}

        else:
            raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

        return payload


class FanSpeed(_action):
    """ 팬 속도 조절 액션 전처리 """

    async def pre_process(self, data, params):

        state = self.state

        # climate 도메인
        if state.domain == climate.DOMAIN:
            if self.state.attributes.get(climate.ATTR_FAN_MODES) is None:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            # 현재 모드 확인
            HA_modes = self.state.attributes.get(climate.ATTR_FAN_MODES)
            clova_modes = {y: x for x, y in FAN_MODES[climate.DOMAIN].items() if y and y in HA_modes}

            current_mode = self.state.attributes.get(climate.ATTR_FAN_MODE)

            # 순서 확인
            if current_mode in HA_modes:
                idx = HA_modes.index(current_mode)
            else:
                raise Exception(ERR_DRIVER_INTERNAL_ERROR)

            # 모드 설정
            if (prefix := data.prefix) == PREFIX_CHANGE:
                next_mode = HA_modes[idx+1 if idx+1 < len(HA_modes) else 0]

            elif prefix == PREFIX_DECREMENT:
                next_mode = HA_modes[idx-1 if idx > 0 else 0]

            elif prefix == PREFIX_INCREMENT:
                next_mode = HA_modes[idx+1 if idx+1 < len(HA_modes) else -1]

            elif prefix == PREFIX_SET:
                next_mode = FAN_MODES[climate.DOMAIN].get(params[ATTR_FAN_SPEED][ATTR_VALUE])

                if not next_mode:
                    next_mode = HA_modes[0]

            else:
                raise Exception(ERR_DRIVER_INTERNAL_ERROR)

            # 액션 실행
            if next_mode != current_mode:
                await self.hass.services.async_call(
                    climate.DOMAIN,
                    climate.SERVICE_SET_FAN_MODE,
                    {
                        ATTR_ENTITY_ID: self.state.entity_id,
                        climate.ATTR_FAN_MODE: next_mode,
                    },
                    blocking=True,
                )

            # 응답 메시지 작성
            payload = {}

            if (prev_mode := clova_modes.get(current_mode)) and prefix in [PREFIX_INCREMENT, PREFIX_DECREMENT]:
                payload[ATTR_PREVIOUS_STATE] = {ATTR_FAN_SPEED: {ATTR_VALUE:prev_mode}}

            if current_mode := clova_modes.get(next_mode):
                payload[ATTR_FAN_SPEED] = {ATTR_VALUE:current_mode}

        # fan 도메인
        elif state.domain == fan.DOMAIN:

            # 현재 퍼센트 확인
            current_percent = self.state.attributes.get(fan.ATTR_PERCENTAGE)

            # 퍼센트 설정

            filds = {ATTR_ENTITY_ID: self.state.entity_id}

            if (prefix := data.prefix) == PREFIX_INCREMENT:
                service = fan.SERVICE_INCREASE_SPEED

            elif prefix == PREFIX_DECREMENT:
                service = fan.SERVICE_DECREASE_SPEED

            elif prefix == PREFIX_SET:
                next_percent = [x for x in FAN_MODES[fan.DOMAIN] if x >= current_percent][0]
                filds[fan.ATTR_PERCENTAGE] = next_percent
                service = fan.SERVICE_SET_PERCENTAGE

            else:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            # 액션 실행
            await self.hass.services.async_call(
                fan.DOMAIN,
                service,
                filds,
                blocking=True,
            )

            # 응답 메시지 작성
            payload = {}

        else:
            raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

        return payload


class TargetTemperature(_action):
    """ 온도 조절 액션 전처리 """

    async def pre_process(self, data, params):

        if (target_temperature := self.state.attributes.get(ATTR_TEMPERATURE)) is None:
            raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

        # 온도 확인
        target_temperature = int(target_temperature)
        set_target_temperature = target_temperature

        # 최대/최소 온도 확인
        min_temp = int(self.state.attributes.get(climate.ATTR_MIN_TEMP, 7))
        max_temp = int(self.state.attributes.get(climate.ATTR_MAX_TEMP, 35))

        # 온도 설정
        if (prefix := data.prefix) == PREFIX_SET:
            set_target_temperature = params[ATTR_TARGET_TEMPERATURE][ATTR_VALUE]

        elif prefix == PREFIX_INCREMENT:
            set_target_temperature += params[ATTR_DELTA_TEMPERATURE][ATTR_VALUE]

            if set_target_temperature > max_temp:
                set_target_temperature = max_temp

        elif prefix == PREFIX_DECREMENT:
            set_target_temperature -= params[ATTR_DELTA_TEMPERATURE][ATTR_VALUE]

            if set_target_temperature < min_temp:
                set_target_temperature = min_temp

        # 액션 실행
        if  target_temperature != set_target_temperature:
            await self.hass.services.async_call(
                climate.DOMAIN,
                climate.SERVICE_SET_TEMPERATURE,
                {
                    ATTR_ENTITY_ID: self.state.entity_id,
                    ATTR_TEMPERATURE: set_target_temperature,
                },
                blocking=True,
            )

        # 응답 메시지 작성
        payload = {}
        payload[ATTR_TARGET_TEMPERATURE] = {ATTR_VALUE: set_target_temperature}

        if prefix  in [PREFIX_GET]:
            payload[ATTR_APPLIANCE_RESPONSE_TIMESTAMP] = datetime.now().astimezone().replace(microsecond=0).isoformat()

        elif prefix in [PREFIX_INCREMENT, PREFIX_DECREMENT]:
            payload[ATTR_PREVIOUS_STATE] = {ATTR_TARGET_TEMPERATURE: {ATTR_VALUE: target_temperature}}

        return payload


@register_action
class GetCurrentTemperature(_action):
    """ 온도 확인 액션 """

    name = "GetCurrentTemperature"

    @staticmethod
    def supported(domain, features, device_class, attributes):
        if attributes.get(climate.ATTR_CURRENT_TEMPERATURE) is None:
            return False
        return domain in _ACTIONS["GetCurrentTemperature"].domain

    async def execute(self, data, params):

        if (current_temperature := self.state.attributes.get(climate.ATTR_CURRENT_TEMPERATURE)) is None:
            raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

        payload = {}
        payload[ATTR_CURRENT_TEMPERATUE] = {ATTR_VALUE: int(current_temperature)}
        payload[ATTR_APPLIANCE_RESPONSE_TIMESTAMP] = datetime.now().astimezone().replace(microsecond=0).isoformat()

        return payload


@register_action
class GetDeviceState(_action):
    """ 상태 확인 액션 """

    name = "GetDeviceState"

    @staticmethod
    def supported(domain, features, device_class, attributes):
        if (
                (domain == climate.DOMAIN and attributes.get(climate.ATTR_CURRENT_TEMPERATURE) is None)
                or
                (domain == fan.DOMAIN and attributes.get(fan.ATTR_PERCENTAGE ) is None)
            ):
            return False
        return domain in _ACTIONS["GetDeviceState"].domain

    async def execute(self, data, params):

        state = self.state

        payload = {}
        devices = []
        device = {}

        # climate 도메인
        if state.domain == climate.DOMAIN:

            current_temperature = state.attributes.get(climate.ATTR_CURRENT_TEMPERATURE)

            device[ATTR_NAME] = TRANSLATION_ONDO
            device[ATTR_VALUE] = int(current_temperature)
            device[ATTR_UNIT] = "celsius"

        # fan 도메인
        elif state.domain == fan.DOMAIN:

            speed = state.attributes.get(fan.ATTR_PERCENTAGE)

            device[ATTR_NAME] = TRANSLATION_SOGDO
            device[ATTR_VALUE] = int(speed)
            device[ATTR_UNIT] = "percentage"

        else:
            raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

        # 응답 메시지 작성
        devices.append(device)
        payload[ATTR_STATES] = devices
        payload[ATTR_APPLIANCE_RESPONSE_TIMESTAMP] = datetime.now().astimezone().replace(microsecond=0).isoformat()

        return payload


class Oscillation(_action):
    """ 스윙 모드 액션 전처리"""

    async def pre_process(self, data, params):

        # climate 도메인
        if self.state.domain == climate.DOMAIN:

            if self.state.attributes.get(climate.ATTR_SWING_MODES) is None:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            HA_modes = [_ for _ in self.state.attributes.get(climate.ATTR_SWING_MODES) if _ != climate.SWING_OFF]
            clova_modes = {y: x for x, y in SWING_MODES.items() if y and y in HA_modes}

            current_mode = self.state.state

            # 순서 확인
            if current_mode in HA_modes:
                idx = HA_modes.index(current_mode)

            elif current_mode == climate.SWING_OFF:
                idx = -1

            else:
                raise Exception(ERR_DRIVER_INTERNAL_ERROR)

            # 모드 설정
            if (prefix := data.prefix) == PREFIX_START:
                next_mode = HA_modes[idx+1 if idx+1 < len(HA_modes) else 0]

            elif prefix == PREFIX_STOP:
                next_mode = climate.SWING_OFF

            else:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            # 액션 실행
            if next_mode != current_mode:
                await self.hass.services.async_call(
                    climate.DOMAIN,
                    climate.SERVICE_SET_SWING_MODE,
                    {
                        ATTR_ENTITY_ID: self.state.entity_id,
                        climate.ATTR_SWING_MODE: next_mode,
                    },
                    blocking=True,
                )


        # fan 도메인
        if self.state.domain == fan.DOMAIN:

            if self.state.attributes.get(fan.ATTR_OSCILLATING) is None:
                raise Exception(ERR_UNSUPPORTED_OPERATION_ERROR)

            # 액션 실행
            if next_mode != current_mode:
                await self.hass.services.async_call(
                    fan.DOMAIN,
                    fan.SERVICE_OSCILLATE,
                    {
                        ATTR_ENTITY_ID: self.state.entity_id,
                        fan.ATTR_OSCILLATING: data.prefix == PREFIX_START,
                    },
                    blocking=True,
                )
        # 응답 메시지 작성
        payload = {}

        return payload



""" 클래스 작성 베이스 템플릿 """
BASE_ACTION_TEMPLATE = '''

@register_action
class {0}{1}({1}, _action):

    name = "{0}{1}"

    @staticmethod
    def supported(domain, features, device_class, attributes):
        return domain in _ACTIONS["{0}{1}"].domain and {2}

    async def execute(self, data, params):
        return await self.pre_process(data, params);
'''

""" ON/OFF 액션 """
exec(''.join(BASE_ACTION_TEMPLATE.replace("({1}, _action)", "({0}, _action)").format("Turn", _, "True", "{}")
for _ in [SUFFIX_ON, SUFFIX_OFF]))


""" 모드 전환 액션 """
exec(''.join(BASE_ACTION_TEMPLATE.format(_, "Mode", '''(
( domain == climate.DOMAIN ) or
( (domain == fan.DOMAIN) and (features & fan.FanEntityFeature.PRESET_MODE) )
)''', "{}")
for _ in [PREFIX_SET, PREFIX_CHANGE]))


""" 팬 속도 조절 액션 """
exec(''.join(BASE_ACTION_TEMPLATE.format(_, "FanSpeed", '''(
( (features & climate.ClimateEntityFeature.FAN_MODE) and (domain == climate.DOMAIN) ) or
( (features & fan.FanEntityFeature.SET_SPEED) and (domain == fan.DOMAIN) )
)''', "{}") for _ in [PREFIX_SET, PREFIX_CHANGE, PREFIX_INCREMENT, PREFIX_DECREMENT]))


""" 온도 조절 액션 """
exec(''.join(BASE_ACTION_TEMPLATE.format(_,"TargetTemperature", "(features & climate.ClimateEntityFeature.TARGET_TEMPERATURE) ", "{}")
for _ in [PREFIX_SET, PREFIX_GET, PREFIX_INCREMENT, PREFIX_DECREMENT]))


""" 스윙 모드 액션 """
exec(''.join(BASE_ACTION_TEMPLATE.format( _, "Oscillation", '''(
( (features & climate.ClimateEntityFeature.SWING_MODE) and (domain == climate.DOMAIN) ) or
( (features & fan.FanEntityFeature.OSCILLATE) and (domain == fan.DOMAIN) )
)''', "{}")
for _ in [PREFIX_START, PREFIX_STOP]))