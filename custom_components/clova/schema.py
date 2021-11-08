""" CLOVA Home extension 스키마"""
from __future__ import annotations

import logging
import re
from collections.abc import Callable
from typing import Any
from datetime import datetime

import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.const import CONF_NAME, CONF_ENTITY_ID, CONF_SERVICE, CONF_SERVICE_DATA

from .const import (
    CONF_ACTION,
    CONF_ACTION_DETAILS,
    CONF_ACTIONS,
    CONF_ALLOWABLE_VALUE,
    CONF_APPLIANCE_ID,
    CONF_CUSTOM_COMMANDS,
    CONF_DATA,
    CONF_DESCRIPTION,
    CONF_ENTITY_CONFIG,
    CONF_ENUM_VALUES,
    CONF_EXPOSE,
    CONF_EXPOSE_BY_DEFAULT,
    CONF_EXPOSED_DOMAINS,
    CONF_IR,
    CONF_LOCATION,
    CONF_MANUFACTURER,
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    CONF_MODEL,
    CONF_RESPONSE,
    CONF_TAGS,
    CONF_TYPE,
    CONF_VERSION,
    DEFAULT_EXPOSE_BY_DEFAULT,
    DEFAULT_EXPOSED_DOMAINS,
    DEFAULT_IR,
    DEVICE_TYPE,
    ACTIONS,
    DOMAIN_TO_CLOVA_TYPES,
    DEVICE_CLASS_TO_CLOVA_TYPES
)

_LOGGER = logging.getLogger(__name__)


ACTIONS = [x for x in ACTIONS if x != "DiscoverAppliances"]


def action_details_schema_validate(obj: dict) -> Callable[[dict], dict]:
    """ 액션 세부사항 스키마 유효성 검사 """
    
    if not isinstance(obj, dict):
        raise vol.Invalid("dictionary 형식이 아닙니다.")

    # 데이터 키가 있으면 서비스 키도 존재하는지 검사 
    if obj.get(CONF_SERVICE_DATA) and not obj.get(cv.CONF_SERVICE):
        raise vol.Invalid(f"서비스({cv.CONF_SERVICE})를 입력하세요.")

    # allowable_value 키의 값이 유효한지 검사 """
    if allowable := obj.get(CONF_ALLOWABLE_VALUE):

        if (type := allowable.get(CONF_TYPE)) == "string" and allowable.get(CONF_ENUM_VALUES):
            for v in allowable.get(CONF_ENUM_VALUES):
                if not isinstance(v, str):
                    raise vol.Invalid(f" \"{CONF_TYPE}\"의 값이 \"{type}\"이라면 \"{CONF_ENUM_VALUES}\"는 문자 배열 형식이 되어야 합니다.")

        elif (type := allowable.get(CONF_TYPE)) == "number" and allowable.get(CONF_ENUM_VALUES):
            for v in allowable.get(CONF_ENUM_VALUES):
                if not isinstance(v, int):
                    raise vol.Invalid(f"\"{CONF_TYPE}\"의 값이 \"{type}\"이라면 \"{CONF_ENUM_VALUES}\"는 숫자 배열 형식이 되어야 합니다.")

        elif (type := allowable.get(CONF_TYPE)) == "number":
            if not (allowable.get(CONF_MIN_VALUE) and allowable.get(CONF_MAX_VALUE)):
                raise vol.Invalid(f"\"{CONF_TYPE}\"의 값이 \"{type}\"이라면 \"{CONF_MIN_VALUE}\"와 \"{CONF_MAX_VALUE}\"는 반드시 포함해야합니다.")

    return obj


def device_type_validate(obj: dict) -> Callable[[dict], dict]:
    """ 디바이스에 따라 허용되는 액션 검사 """
     
    if not isinstance(obj, dict):
        raise vol.Invalid("dictionary 형식이 아닙니다.")

    for entity_id in obj:

        domain = entity_id.split(".", 1)[0]

        if (typ := obj.get(entity_id, {}).get(CONF_TYPE)) is None:
            typ = DOMAIN_TO_CLOVA_TYPES.get(domain)

        if typ is None:
            typ = DEVICE_CLASS_TO_CLOVA_TYPES.get(domain)

        if typ is None:
            raise vol.Invalid(f"지원하지 않는 타입(type)입니다..")
        
        if action_details := obj.get(entity_id, {}).get(CONF_ACTION_DETAILS):
            if (action := list(action_details.keys())[0]) not in DEVICE_TYPE.get(typ.upper()):
                if obj.get(entity_id, {}).get(CONF_TYPE) is None:
                    typ = domain
                raise vol.Invalid(f"\"{typ}\" 도메인은 \"{action}\" 액션을 지원하지 않습니다.")
    
    return obj




def custom_commands_action_validate(obj: dict) -> Callable[[dict], dict]:
    """ 커스텀 명령어 액션 유효성 검사 """
    
    if not isinstance(obj, dict):
        raise vol.Invalid("dictionary 형식이 아닙니다.")
    
    entity_config = obj.get(CONF_ENTITY_CONFIG, {})
    
    for command in obj.get(CONF_CUSTOM_COMMANDS,[]):

        for actions in command.get(CONF_ACTIONS, []):

            domain = actions[CONF_ENTITY_ID].split(".", 1)[0]
            action = actions[CONF_ACTION]
            entity_id = actions[CONF_ENTITY_ID]

            if entity_config.get(entity_id, {}).get(CONF_ACTION_DETAILS, {}).get(action):
                continue

            elif (typ := DOMAIN_TO_CLOVA_TYPES.get(domain)) and action in DEVICE_TYPE.get(typ,[]):
                continue

            elif (typ := DEVICE_CLASS_TO_CLOVA_TYPES.get(domain)) and DEVICE_TYPE.get(typ):
                 continue

            else:
                raise vol.Invalid(f"custom_commands 에러: \"{action}\" 액션은 \"{entity_id}\" 구성요소에서 지원하지 않습니다.")

    return obj



SET_BRIGHTNESS_SCHEMA = vol.Schema(
    {
        vol.Optional("brightness"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
        }
    }
)


SET_CHANNEL_SCHEMA = vol.Schema(
    {
        vol.Optional("channel"): {
            vol.Required("value"): vol.Coerce(int)
        },
        vol.Optional("subChannel"): {
            vol.Required("value"): vol.Coerce(int)
        }
    }, extra=vol.ALLOW_EXTRA
)


SET_CHANNEL_BY_NAME_SCHEMA = vol.Schema(
    {
        vol.Optional("channelName"): {
            vol.Required("value"): cv.string
        }
    }, extra=vol.ALLOW_EXTRA
)


SET_COLOR_SCHEMA = vol.Schema(
    {
        vol.Optional("color"): {
            vol.Required("hue"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Required("saturation"): vol.All(vol.Coerce(int), vol.Range(min=0, max=360)),
            vol.Required("brightness"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
        }
    }, extra=vol.ALLOW_EXTRA
)


SET_COLOR_TEMPERATURE_SCHEMA = vol.Schema(
    {
        vol.Optional("colorTemperature"): {
            vol.Required("value"): vol.Coerce(int)
        }
    }, extra=vol.ALLOW_EXTRA
)


SET_FAN_SPEED_SCHEMA = vol.Schema(
    {
        vol.Optional("fanSpeed"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=1, max=3)),
        }
    }, extra=vol.ALLOW_EXTRA
)


SET_LOCK_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("lockState"): vol.In(["LOCKED", "UNLOCKED"])
    }, extra=vol.ALLOW_EXTRA
)


SET_MODE_SCHEMA = vol.Schema(
    {
        vol.Optional("mode"): cv.string
    }, extra=vol.ALLOW_EXTRA
)


SET_TARGET_TEMPERATURE_SCHEMA = vol.Schema(
    {
        vol.Optional("targetTemperature"): {
            vol.Required("value"): vol.Coerce(int),
        },
        vol.Optional("endpoint"): {
            vol.Required("value"): cv.string
        }
    }, extra=vol.ALLOW_EXTRA
)


DECREMENT_BRIGHTNESS_SCHEMA = vol.Schema(
    {
        vol.Optional("brightness"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
        },
        vol.Optional("previousState"): {
            vol.Optional("brightness"): {
                vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            }
        }
    }, extra=vol.ALLOW_EXTRA
)


DECREMENT_CHANNEL_SCHEMA = vol.Schema(
    {
        vol.Optional("channel"): {
            vol.Required("value"): vol.Coerce(int),
        },
        vol.Optional("subChannel"): {
            vol.Required("value"): vol.Coerce(int),
        },
        vol.Optional("previousState"): {
            vol.Optional("channel"): {
                vol.Required("value"): vol.Coerce(int),
            },
            vol.Optional("subChannel"): {
                vol.Required("value"): vol.Coerce(int),
            }
        }
    }, extra=vol.ALLOW_EXTRA
)


DECREMENT_FAN_SPEED_SCHEMA = vol.Schema(
    {
        vol.Optional("fanSpeed"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=1, max=3)),
        },
        vol.Optional("previousState"): {
            vol.Optional("fanSpeed"): {
                vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=1, max=3)),
            }
        }
    }, extra=vol.ALLOW_EXTRA
)


DECREMENT_INTENSITY_LEVEL_SCHEMA = vol.Schema(
    {
        vol.Optional("intensityLevel"): {
            vol.Required("value"): vol.Coerce(int),
        },
        vol.Optional("previousState"): {
            vol.Optional("intensityLevel"): {
                vol.Required("value"): vol.Coerce(int),
            }
        }
    }, extra=vol.ALLOW_EXTRA
)


DECREMENT_TARGET_TEMPERATURE_SCHEMA = vol.Schema(
    {
        vol.Optional("targetTemperature"): {
            vol.Required("value"): vol.Coerce(int),
        },
        vol.Optional("previousState"): {
            vol.Optional("targetTemperature"): {
                vol.Required("value"): vol.Coerce(int),
            }
        }
    }, extra=vol.ALLOW_EXTRA
)


DECREMENT_VOLUME_SCHEMA = vol.Schema(
    {
        vol.Optional("targetVolume"): {
            vol.Required("value"): vol.Coerce(int),
        },
        vol.Optional("previousState"): {
            vol.Optional("targetVolume"): {
                vol.Required("value"): vol.Coerce(int),
            }
        }
    }, extra=vol.ALLOW_EXTRA
)


INCREMENT_BRIGHTNESS_SCHEMA = DECREMENT_BRIGHTNESS_SCHEMA

INCREMENT_CHANNEL_SCHEMA = DECREMENT_CHANNEL_SCHEMA

INCREMENT_FAN_SPEED_SCHEMA = DECREMENT_FAN_SPEED_SCHEMA
 
INCREMENT_INTENSITY_LEVEL_SCHEMA = DECREMENT_INTENSITY_LEVEL_SCHEMA
   
INCREMENT_TARGET_TEMPERATURE_SCHEMA = DECREMENT_TARGET_TEMPERATURE_SCHEMA
 
INCREMENT_VOLUME_SCHEMA = DECREMENT_VOLUME_SCHEMA


CHANGE_FAN_SPEED_SCHEMA = vol.Schema(
    {
        vol.Optional("fanSpeed"): {
            vol.Required("value"): vol.In([1,2,3])
        }
    }, extra=vol.ALLOW_EXTRA
)


CHANGE_MODE_SCHEMA = vol.Schema(
    {
        vol.Optional("mode"): {
            vol.Required("value") : cv.string
        },
        vol.Optional("previousState"): {
            vol.Optional("mode"): {
                vol.Required("value"): cv.string
            }
        }
    }
)


PREHEAT_SCHEMA = vol.Schema(
    {
        vol.Optional("targetTemperature"): {
            vol.Required("value") : int
        }
    }
)


RELEASE_MODE_SCHEMA = CHANGE_MODE_SCHEMA


STOP_SCHEMA = vol.Schema(
    {
        vol.Optional("phase"): {
            vol.Required("value") : cv.string
        }
    }
)


GET_AIR_QUALITY_SCHEMA = vol.Schema(
    {
        vol.Required("airQuality"): {
            vol.Required("index"): vol.In(["good", "normal", "bad", "verybad"])
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_ASLEEP_DURATION_SCHEMA = vol.Schema(
    {
        vol.Required("asleepDuration"): cv.string,
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_BMI_SCHEMA = vol.Schema(
    {
        vol.Required("bmi"): {
            vol.Required("value"): vol.Coerce(float)
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_BATTERY_INFO_SCHEMA = vol.Schema(
    {
        vol.Required("batteryInfo"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_BODY_FAT_SCHEMA = vol.Schema(
    {
        vol.Required("bodyFatPercentage"): {
            vol.Required("value"): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
        }, 
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_CLEANING_CYCLE_SCHEMA = vol.Schema(
    {
        vol.Required("remainingTime"): {
            vol.Required("value"): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
        }, 
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string        
    }, extra=vol.ALLOW_EXTRA
)


GET_CLOSE_TIME_SCHEMA = vol.Schema(
    {
        vol.Required("closeTimestamp"): cv.string,
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_CONSUMPTION_SCHEMA = vol.Schema(
    {
        vol.Required("consumption"): vol.All(
            [
                vol.Schema(
                    {
                        vol.Required("name"): cv.string,
                        vol.Required("value"): vol.Coerce(float),
                        vol.Required("unit", default="L"): vol.In(["KL", "kl", "L", "l", "cc", "KW", "kw", "W"])
                    }
                )
            ]
        )
    }, extra=vol.ALLOW_EXTRA
)


GET_CURRENT_BILL_SCHEMA = vol.Schema(
    {
         vol.Required("currentBill"): {
            vol.Required("value"): vol.Coerce(int),
            vol.Required("currenvy"): cv.currency
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_CURRENT_SITTING_STATE_SCHEMA =  vol.Schema(
    {
        vol.Required("sittingState"): {
            vol.Required("value"): cv.boolean
        },
        vol.Optional("recentlySittingPeriod"): {
            "start" : cv.string,
            "end" : cv.string
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_CURRENT_TEMPERATURE_SCHEMA = vol.Schema(
    {
        vol.Required("currentTemperature"): {
            vol.Required("value"): vol.Coerce(int)
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_DETECTED_TIME_SCHEMA = vol.Schema(
    {
        vol.Required("detectedTime"): {
            vol.Required("value"): cv.string
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_DETECTION_COUNT_SCHEMA = vol.Schema(
    {
        vol.Required("detectionCount"): {
            vol.Required("value"): cv.string
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_DEVICE_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("states"): vol.All(
            [
                {
                    vol.Required("name"): cv.string,
                    vol.Required("value"): vol.Any(int, cv.string),
                    vol.Optional("unit", default="celsius"): vol.In(["celsius", "percentage"])
                }
            ]
        )
    }, extra=vol.ALLOW_EXTRA
)


GET_ESTIMATE_BILL_SCHEMA = vol.Schema(
    {
         vol.Required("estimateBill"): {
            vol.Required("value"): vol.Coerce(int),
            vol.Required("currenvy"): cv.currency
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_ESTIMATE_CONSUMPTION_SCHEMA = vol.Schema(
    {
        vol.Required("states"): vol.All(
            [
                {
                    vol.Required("name"): cv.string,
                    vol.Required("value"): vol.Coerce(int),
                    vol.Optional("unit", default="KW"): vol.In(["KW", "kw", "W"])
                }
            ]
        ),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_EXPENDABLE_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("expendableInfo"): vol.All([
            vol.Any(
                vol.Schema({
                    vol.Required("name") : cv.string,
                    vol.Optional("remainingTime") : cv.string, 
                }),
                vol.Schema({
                    vol.Required("name"): cv.string,
                    vol.Optional("usage"): {
                        vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
                        vol.Optional("unit", default="percentage"): vol.In(["celsius", "percentage"])
                    }
                })
            )
        ]),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_FINE_DUST_SCHEMA = vol.Schema(
    {
        vol.Required("findDust"): {
            vol.Optional("value"): vol.Coerce(int),
            vol.Required("index"): vol.In(["good", "normal", "bad", "verybad"])
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_HEALTH_SCORE_SCHEMA = vol.Schema(
    {
        vol.Required("healthScore"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_HUMIDITY_SCHEMA = vol.Schema(
    {
        vol.Required("humidity"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_KEEP_WARM_TIME_SCHEMA = vol.Schema(
    {
        vol.Required("keepWarmTime"): cv.string,
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_LOCK_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("lockState"): vol.In(["LOCKED", "UNLOCKED"]),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_MUSCLE_SCHEMA = vol.Schema(
    {
        vol.Required("musclePercentage"): {
            vol.Required("value"): vol.Coerce(float)
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_NOTICE_RESPONSE = vol.Schema(
    {
        vol.Required("notice"): vol.All([cv.string]),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_OPEN_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("OpenState"): vol.In(["CLOSED", "OPENED"]),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_OPEN_TIME_SCHEMA = vol.Schema(
    {
        vol.Required("openTimestamp"): cv.string,
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_PACKAGE_SCHEMA = vol.Schema(
    {
        vol.Required("package"): vol.All([cv.string]),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_PHASE_SCHEMA = vol.Schema(
    {
        vol.Required("phase"): {
            vol.Required("value"): cv.string
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_POWER_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("powerState"): {
            vol.Required("value"): cv.string
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_PROGRESSIVE_TAX_BRACKET_SCHEMA = vol.Schema(
    {
        vol.Required("progressiveTaxBracket"): {
            vol.Required("value"): vol.Coerce(int)
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_REMAINING_TIME_SCHEMA = vol.Schema(
    {
        vol.Required("remainingTime"): cv.string,
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_RIGHT_POSTURE_RATIO_SCHEMA = vol.Schema(
    {
        vol.Required("rightPostureRatio"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_SLEEP_SCORE_SCHEMA = vol.Schema(
    {
        vol.Required("sleepScore"): {
            vol.Required("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_SLEEP_START_TIME_SCHEMA = vol.Schema(
    {
        vol.Required("startTimestampList"):vol.All([cv.string]),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_TARGET_TEMPERATURE_SCHEMA = vol.Schema(
    {
        vol.Required("targetTemperature"):{
            vol.Required("value"): vol.Coerce(int),
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_ULTRA_FINE_DUST_SCHEMA = vol.Schema(
    {
        vol.Required("ultraFineDust"):{
            vol.Optional("value"): vol.All(vol.Coerce(int), vol.Range(min=0, max=100)),
            vol.Required("index"): vol.In(["good", "normal", "bad", "verybad"])
        },
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_USAGE_TIME_SCHEMA = vol.Schema(
    {
        vol.Required("usageTime"):cv.string,
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_VEHICLE_LOCATION_SCHEMA = vol.Schema(
    {
        vol.Required("vehicleLocationList"): vol.All([
            vol.Schema({
                vol.Required("name"): cv.string,
                vol.Required("value"): cv.string,
            })
        ]),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


GET_WEIGHT_SCHEMA = vol.Schema(
    {
        vol.Required("weight"): vol.All([
            vol.Schema({
                vol.Required("value"): vol.Coerce(float)
            })
        ]),
        vol.Optional("applianceResponseTimestamp", 
            default=datetime.now().astimezone().replace(microsecond=0).isoformat()
        ): cv.string
    }, extra=vol.ALLOW_EXTRA
)


HEALTH_CHECK_SCHEMA = vol.Schema(
    {
        vol.Required("isReachable"): cv.boolean,
        vol.Required("isReachable"): cv.boolean,
    }, extra=vol.ALLOW_EXTRA
)


def response_validate(obj: dict) -> Callable[[dict], dict]:
    """ 응답 메시지 유효성 검사 """
    
    if not isinstance(obj, dict):
        raise vol.Invalid("dictionary 형식이 아닙니다.")

    for action, v in obj.items():

        schema = re.sub(r"([^A-Z]+)([A-Z])", r"\1_\2", action).upper() + "_SCHEMA"
        
        if (SCHEMA := globals().get(schema)) and (response := v.get(CONF_RESPONSE)):
            _LOGGER.error(response)
            SCHEMA(response)

    return obj


ACTION_DETAILS_SCHEMA = {
    vol.Required(vol.In(ACTIONS)): vol.All(
        {
            vol.Optional(cv.CONF_SERVICE, "service name"): vol.Any(cv.service, cv.dynamic_template),
            vol.Optional(CONF_SERVICE_DATA): vol.Any(cv.template, vol.All(dict, cv.template_complex)),
            vol.Required(CONF_RESPONSE, default={}): vol.Any(cv.template, vol.All(dict, cv.template_complex)),
            vol.Optional(CONF_ALLOWABLE_VALUE): {
                vol.Required(CONF_TYPE): vol.In(["string","number","boundedNumber"]),
                vol.Optional(CONF_MIN_VALUE): vol.Coerce(int),
                vol.Optional(CONF_MAX_VALUE): vol.Coerce(int),
                vol.Optional(CONF_ENUM_VALUES): list
            }
        },
        action_details_schema_validate,
    )
}


ENTITY_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_EXPOSE, default=True): cv.boolean,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_MANUFACTURER):cv.string,
        vol.Optional(CONF_MODEL):cv.string,
        vol.Optional(CONF_VERSION): cv.string,
        vol.Optional(CONF_DESCRIPTION): cv.string,
        vol.Optional(CONF_IR, default=DEFAULT_IR): cv.boolean,
        vol.Optional(CONF_LOCATION): cv.string,
        vol.Optional(CONF_TYPE): vol.In([ x.lower() for x in DEVICE_TYPE] + [ x.upper() for x in DEVICE_TYPE]),
        vol.Optional(CONF_TAGS): cv.ensure_list(cv.string),
        vol.Optional(CONF_ACTION_DETAILS): ACTION_DETAILS_SCHEMA
    }
)


CLOVA_SCHEMA = vol.All(
    {
        vol.Optional(CONF_EXPOSE_BY_DEFAULT, default=DEFAULT_EXPOSE_BY_DEFAULT): cv.boolean,
        vol.Optional(CONF_EXPOSED_DOMAINS, default=DEFAULT_EXPOSED_DOMAINS): cv.ensure_list,
        vol.Optional(CONF_ENTITY_CONFIG): vol.All( { cv.entity_id: ENTITY_SCHEMA }, device_type_validate ),
        vol.Optional(CONF_CUSTOM_COMMANDS): [{
            vol.Required(CONF_NAME): cv.string,
            vol.Required(CONF_ACTIONS): [{
                vol.Required(CONF_ENTITY_ID): cv.entity_id,
                vol.Required(CONF_ACTION): vol.In(ACTIONS), 
            }]
        }]
    },
    custom_commands_action_validate
)