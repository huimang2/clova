"""CLOVA Home extension 상수"""

import re
from collections import namedtuple

from homeassistant.components import (
    binary_sensor,
    camera,
    climate,
    cover,
    fan,
    group,
    humidifier,
    input_boolean,
    light,
    lock,
    media_player,
    switch,
    vacuum,
)

from homeassistant.components.climate.const import (
    HVAC_MODE_AUTO,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY, 
    HVAC_MODE_FAN_ONLY, 
    HVAC_MODE_HEAT, 
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    SWING_VERTICAL,
    SWING_HORIZONTAL
)

DOMAIN = "clova"

CLOVA_API_ENDPOINT = "/api/clova"

SIGNATURE_PUBLIC_KEY = b"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3BPYiDHfKOMiTcEkukLr
YB1OEicGjxTSI8N5b5ZMxKDtpf4gWTI/+2pXd6e0AZBQJwjXisBAJ4lH8NbiuEpb
8AMIs9iOfTRWvuuw9TBmBBtbUcozVonok/bILTMJaz8jpA/hSb8id5/UmoTyV8Cm
sHC56IUtNrS06mLydeThr5WVI1K6fbmYudpBG8vJBAPC2j+Fh+TwfyJ5Xh6bLabz
2IyqeyG63D6eYpWRB4vBZ4lck1mXDnQvFqRa3LkhoGi/LoCEvo0HxhR49B25qfdR
tZPLfboZgb5k29XSrOZbrAWrM/v5Zn5mdTrFubBd65wz3+VyJhS0nPmcTPCLCo4q
9QIDAQAB
-----END PUBLIC KEY-----
"""

ATTR_ACCESS_TOKEN = "accessToken"
ATTR_ACTIONS = "actions"
ATTR_ADDITIONAL_APPLIANCE_DETAILS = "additionalApplianceDetails"
ATTR_APPLIANCE = "appliance"
ATTR_APPLIANCE_ID = "applianceId"
ATTR_APPLIANCE_RESPONSE_TIMESTAMP = "applianceResponseTimestamp"
ATTR_APPLIANCE_TYPES = "applianceTypes"
ATTR_CURRENT_TEMPERATUE = "currentTemperature"
ATTR_CUSTOM_COMMANDS = "customCommands"
ATTR_DIRECTION = "direction"
ATTR_DISCOVERED_APPLIANCES = "discoveredAppliances"
ATTR_DELTA_TEMPERATURE = "deltaTemperature"
ATTR_FAN_SPEED = "fanSpeed"
ATTR_FRIENDLY_NAME = "friendlyName"
ATTR_HEADER = "header"
ATTR_IS_IR = "isIr"
ATTR_IS_REACHABLE = "isReachable"
ATTR_IS_TURN_ON = "isTurnOn"
ATTR_LOCATION = "location"
ATTR_NAME = "name"
ATTR_NAMESPACE = "namespace"
ATTR_MANUFACTURE_NAME = "manufacturerName"
ATTR_MESSAGE_ID = "messageId"
ATTR_MODE = "mode"
ATTR_MODEL_NAME = "modelName"
ATTR_PAYLOAD = "payload"
ATTR_PAYLOAD_VERSION = "payloadVersion"
ATTR_PREVIOUS_STATE = "previousState"
ATTR_SIGNATURECEK = "signaturecek"
ATTR_STATES = "states"
ATTR_TARGET_TEMPERATURE = "targetTemperature"
ATTR_UNIT = "unit"

ATTR_VALUE = "value"
ATTR_VERSION = "version"

PREFIX_CHANGE = "Change"
PREFIX_SET = "Set"
PREFIX_GET = "Get"
PREFIX_DECREMENT = "Decrement"
PREFIX_INCREMENT = "Increment"
PREFIX_CALL = "Call"
PREFIX_START = "Start"
PREFIX_STOP = "Stop"

SUFFIX_REQUEST = "Request"
SUFFIX_RESPONSE = "Response"
SUFFIX_CONFIRMATION = "Confirmation"
SUFFIX_OFF = "Off"
SUFFIX_ON = "On"

CONF_EXPOSE = "expose"
CONF_ENTITY_CONFIG = "entity_config"
CONF_EXPOSE_BY_DEFAULT = "expose_by_default"
CONF_EXPOSED_DOMAINS = "exposed_domains"
CONF_LOCATION = "location"

TRANSLATION_ONDO = "온도"
TRANSLATION_SOGDO = "속도"

DEFAULT_EXPOSE_BY_DEFAULT = True
DEFAULT_EXPOSED_DOMAINS = [
    "climate",
    "cover",
    "fan",
    "group",
    "humidifier",
    "light",
    "lock",
    "media_player",
    "switch",
    "vacuum",
]

LOCATION = {
    "다락방": "ATTIC",
    "베란다": "BALCONY",
    "거실베란다": "BALCONY_IN_LIVING_ROOM",
    "안방베란다": "BALCONY_IN_MAIN_ROOM",
    "주방베란다": "BALCONY_KITCHEN",
    "화장실": "BATH_ROOM",
    "거실 화장실": "BATH_ROOM_IN_LIVING_ROOM",
    "안방 화장실": "BATH_ROOM_IN_MAIN_ROOM",
    "침실": "BED_ROOM",
    "큰 화장실": "BIG_BATH_ROOM",
    "큰아이 방": "BIG_CHILD_ROOM",
    "큰 방": "BIG_ROOM",
    "보일러실": "BOILER_ROOM",
    "식당": "DINING_ROOM",
    "드레스룸": "DRESS_ROOM",
    "현관": "ENTRANCE",
    "가족룸": "FAMILY_ROOM",
    "아버님방": "FATHER_ROOM",
    "다섯째 방": "FIFTH_ROOM",
    "첫째 방": "FIRST_ROOM",
    "넷째 방": "FOURTH_ROOM",
    "복도": "HALLWAY",
    "주방": "KITCHEN",
    "서재": "LIBRARY",
    "거실": "LIVING_ROOM",
    "대문": "MAIN_GATE",
    "안방": "MAIN_ROOM",
    "어머님방": "MOTHER_ROOM",
    "내 방": "MY_ROOM",
    "부모님 방": "PARENTS_ROOM",
    "놀이방": "PLAY_ROOM",
    "파우더룸": "POWDER_ROOM",
    "방": "ROOM",
    "둘째 방": "SECOND_ROOM",
    "작은아이 방": "SMALL_CHILD_ROOM",
    "작은 거실": "SMALL_LIVING_ROOM",
    "작은 방": "SMALL_ROOM",
    "작은 주방": "SMALL_KITCHEN",
    "작은 화장실": "SMALL_BATH_ROOM",
    "계단": "STAIRS",
    "셋째 방": "THIRD_ROOM",
    "윗층 방": "UPSTAIRS_ROOM",
    "다용도실": "UTILITY_ROOM",
    "창고": "WAREHOUSE",
    "마당": "YARD",
}

DEVICE_TYPE = [
    "AIRCONDITIONER",
    "AIRPURIFIER",
    "AIRSENSOR",
    "BIDET",
    "BODYWEIGHTSCALE",
    "BUILDING_ELECTRIC_METER",
    "BUILDING_ELEVATOR_CALLER",
    "BUILDING_GAS_METER",
    "BUILDING_HEATING_METER",
    "BUILDING_HOTWATER_METER",
    "BUILDING_NOTICE_MONITOR",
    "BUILDING_PACKAGE",
    "BUILDING_PARKING_MONITOR",
    "BUILDING_UTILITY_BILL_MONITOR",
    "BUILDING_WATER_METER",
    "CLOTHESCAREMACHINE",
    "CLOTHESDRYER",
    "CLOTHESWASHER",
    "DEHUMIDIFIER",
    "DISHWASHER",
    "ELECTRICKETTLE",
    "ELECTRICTOOTHBRUSH",
    "FAN",
    "HEATER",
    "HOMECAM",
    "HUMIDIFIER",
    "KIMCHIREFRIGERATOR",
    "LIGHT",
    "MASSAGECHAIR",
    "MICROWAVE",
    "MOTIONSENSOR",
    "OPENCLOSESENSOR",
    "OVEN",
    "POWERSTRIP",
    "PURIFIER",
    "RANGE",
    "RANGEHOOD",
    "REFRIGERATOR",
    "RICECOOKER",
    "ROBOTVACUUM",
    "SETTOPBOX",
    "SLEEPINGMONITOR",
    "SMARTBED",
    "SMARTCHAIR",
    "SMARTCURTAIN",
    "SMARTHUB",
    "SMARTLOCK",
    "SMARTMETER",
    "SMARTPLUG",
    "SMARTTV",
    "SMARTVALVE",
    "SMOKESENSOR",
    "SWITCH",
    "THERMOSTAT",
    "VENTILATOR",
    "WATERBOILER",
    "WINECELLAR",
]

for s in DEVICE_TYPE:
    globals()['TYPE_{}'.format(s)] = s

DOMAIN_TO_CLOVA_TYPES = {
    camera.DOMAIN: TYPE_HOMECAM,
    climate.DOMAIN: TYPE_AIRCONDITIONER,
    cover.DOMAIN: TYPE_SMARTCURTAIN,
    fan.DOMAIN: TYPE_FAN,
    group.DOMAIN: TYPE_SWITCH,
    humidifier.DOMAIN: TYPE_HUMIDIFIER,
    light.DOMAIN: TYPE_LIGHT,
    lock.DOMAIN: TYPE_SMARTLOCK,
    media_player.DOMAIN: TYPE_SETTOPBOX,
    switch.DOMAIN: TYPE_SWITCH,
    vacuum.DOMAIN: TYPE_ROBOTVACUUM,
}

DEVICE_CLASS_TO_CLOVA_TYPES = {
    (switch.DOMAIN, switch.DEVICE_CLASS_SWITCH): TYPE_SWITCH,
    (binary_sensor.DOMAIN, binary_sensor.DEVICE_CLASS_OPENING): TYPE_OPENCLOSESENSOR,
    (binary_sensor.DOMAIN, binary_sensor.DEVICE_CLASS_WINDOW): TYPE_OPENCLOSESENSOR,
    (media_player.DOMAIN, media_player.DEVICE_CLASS_TV): TYPE_SMARTTV,
    (humidifier.DOMAIN, humidifier.DEVICE_CLASS_HUMIDIFIER): TYPE_HUMIDIFIER,
    (humidifier.DOMAIN, humidifier.DEVICE_CLASS_DEHUMIDIFIER): TYPE_DEHUMIDIFIER,
}

_ACTION = namedtuple("_ACTION", "name prefix suffix domain")
_ACTIONS = [
    _ACTION("AirQuality", [PREFIX_START, PREFIX_STOP], [], []),
    _ACTION("AirQuality", [PREFIX_GET], [], []),
    _ACTION("AsleepDuration", [PREFIX_GET], [], []),
    _ACTION("AwakeDuration", [PREFIX_GET], [], []),
    _ACTION("BatteryInfo", [PREFIX_GET], [], []),
    _ACTION("BMI", [PREFIX_GET], [], []),
    _ACTION("BodyFat", [PREFIX_GET], [], []),
    _ACTION("Brightness", [PREFIX_SET, PREFIX_DECREMENT, PREFIX_INCREMENT], [], []),
    _ACTION("Charge", [], [], []),
    _ACTION("Channel", [PREFIX_SET, PREFIX_DECREMENT, PREFIX_INCREMENT], [], []),
    _ACTION("ChannelByName", [PREFIX_SET], [], []),
    _ACTION("CleaningCycle", [PREFIX_GET], [], []),
    _ACTION("Close", [], [], []),
    _ACTION("CloseTime", [PREFIX_GET], [], []),
    _ACTION("Color", [PREFIX_SET], [], []),
    _ACTION("ColorTemperature", [PREFIX_SET], [], []),
    _ACTION("Consumption", [PREFIX_GET], [], []),
    _ACTION("CurrentBill", [PREFIX_GET], [], []),
    _ACTION("CurrtentSittingState", [PREFIX_GET], [], []),
    _ACTION("CurrentTemperature", [PREFIX_GET], [], ["climate"]),
    _ACTION("DetectionCount", [PREFIX_GET], [], []),
    _ACTION("DetectedTime", [PREFIX_GET], [], []),
    _ACTION("DeviceState", [PREFIX_GET], [], ["climate", "fan"]),
    _ACTION("Elevator", [PREFIX_CALL], [], []),
    _ACTION("EstimateBill", [PREFIX_GET], [], []),
    _ACTION("EstimateConsumption", [PREFIX_GET], [], []),
    _ACTION("ExpendableState", [PREFIX_GET], [], []),
    _ACTION("FanSpeed", [PREFIX_CHANGE, PREFIX_SET, PREFIX_DECREMENT, PREFIX_INCREMENT], [], ["climate", "fan"]),
    _ACTION("FineDust", [PREFIX_GET], [], []),
    _ACTION("HealthCheck", [], [], ["climate", "cover", "fan", "group", "humidifier", "light", "lock", "media_player", "switch", "vacuum"]),
    _ACTION("HealthScore", [PREFIX_GET], [], []),
    _ACTION("Humidity", [PREFIX_GET], [], []),
    _ACTION("InputSource", [PREFIX_CHANGE], [], []),
    _ACTION("IntensityLevel", [PREFIX_DECREMENT, PREFIX_INCREMENT], [], []),
    _ACTION("KeepWarmTime", [PREFIX_GET], [], []),
    _ACTION("LockState", [PREFIX_GET, PREFIX_SET], [], []),
    _ACTION("Lower", [], [], []),
    _ACTION("Mode", [PREFIX_CHANGE, PREFIX_SET], [], ["climate", "fan"]),
    _ACTION("Mute", [], [], []),
    _ACTION("Muscle", [PREFIX_GET], [], []),
    _ACTION("Notice", [PREFIX_GET], [], []),
    _ACTION("Open", [], [], []),
    _ACTION("OpenState", [PREFIX_GET], [], []),
    _ACTION("OpenTime", [PREFIX_GET], [], []),
    _ACTION("Oscillation", [PREFIX_START, PREFIX_STOP], [], ["climate", "fan"]),
    _ACTION("Package", [PREFIX_GET], [], []),
    _ACTION("Phase", [PREFIX_GET], [], []),
    _ACTION("Power", [PREFIX_CHANGE], [], ["climate"]),
    _ACTION("PowerState", [PREFIX_GET], [], []),
    _ACTION("Preheat", [], [], []),
    _ACTION("ProgressiveTaxBracket", [PREFIX_GET], [], []),
    _ACTION("Raise", [], [], []),
    _ACTION("Recording", [PREFIX_START, PREFIX_STOP], [], []),
    _ACTION("ReleaseMode", [], [], []),
    _ACTION("RemainingTime", [PREFIX_GET], [], []),
    _ACTION("RightPostureRatio", [PREFIX_GET], [], []),
    _ACTION("SleepScore", [PREFIX_GET], [], []),
    _ACTION("SleepStartTime", [PREFIX_GET], [], []),
    _ACTION("TargetTemperature", [PREFIX_GET, PREFIX_SET, PREFIX_DECREMENT, PREFIX_INCREMENT], [], ["climate"]),
    _ACTION("Turn", [], [SUFFIX_OFF, SUFFIX_ON], ["climate", "cover", "fan", "group", "humidifier", "light", "lock", "media_player", "switch", "vacuum"]),
    _ACTION("Volume", [PREFIX_DECREMENT, PREFIX_INCREMENT], [], []),
    _ACTION("UltraFineDust", [PREFIX_GET], [], []),
    _ACTION("Unmute", [], [], []),
    _ACTION("UsageTime", [PREFIX_GET], [], []),
    _ACTION("VehicleLocation", [PREFIX_GET], [], []),
    _ACTION("Weight", [PREFIX_GET], [], []),
    _ACTION("DiscoverAppliances", [],[],[]),
]

INTERFACE_DISCOVERY = "DiscoverAppliancesRequest"

INTERFACE_ERROR = [
    "ActionFailedError",
    "ActionTemporarilyBlockedError",
    "ConditionsNotMetError",
    "DeviceConnectionError",
    "DeviceFailureError",
    "DriverInternalError",
    "ExpiredAccessTokenError",
    "InvalidAccessTokenError",
    "NoSuchTargetError",
    "NotSupportedInCurrentModeError",
    "TargetOfflineError",
    "UnsupportedOperationError",
    "ValueNotFoundError",
    "ValueNotSupportedError",
    "ValueOutOfRangeError",
    "ValidationFailedError",
]

for s in INTERFACE_ERROR:
    globals()['ERR_{}'.format(re.sub(r'([A-Z])',r'_\1',s)[1:].upper())] = s


INTERFACE_VALUE_SETTING = [
    "SetBrightnessRequest",
    "SetChannelByNameRequest",
    "SetChannelRequest",
    "SetColorRequest",
    "SetColorTemperatureRequest",
    "SetFanSpeedRequest",
    "SetLockStateRequest",
    "SetModeRequest",
    "SetTargetTemperatureRequest",
]

INTERFACE_INCREMENTAL = [
    "DecrementBrightnessRequest",
    "DecrementChannelRequest",
    "DecrementFanSpeedRequest",
    "DecrementIntensityLevelRequest",
    "DecrementTargetTemperatureRequest",
    "DecrementVolumeRequest",
    "IncrementBrightnessRequest",
    "IncrementChannelRequest",
    "IncrementFanSpeedRequest",
    "IncrementIntensityLevelRequest",
    "IncrementTargetTemperatureRequest",
    "IncrementVolumeRequest",
]

INTERFACE_SWITCHING = [
    "ChangeFanSpeedRequest",
    "ChangeInputSourceRequest",
    "ChangeModeRequest",
    "ChangePowerRequest",
]

INTERFACE_ACTION = [
    "CallElevatorRequest",
    "ChargeRequest",
    "CloseRequest",
    "LowerRequest",
    "MuteRequest",
    "OpenRequest",
    "PreheatRequest",
    "RaiseRequest",
    "ReleaseModeRequest",
    "StartOscillationRequest",
    "StartRecordingRequest",
    "StopRequest",
    "StopOscillationRequest",
    "StopRecordingRequest",
    "TurnOffRequest",
    "TurnOnRequest",
    "UnmuteRequest",
]

INTERFACE_GET = [
    "GetAirQualityRequest",
    "GetAsleepDurationRequest",
    "GetAwakeDurationRequest",
    "GetBMIRequest",
    "GetBatteryInfoRequest",
    "GetBodyFatRequest",
    "GetCleaningCycleRequest",
    "GetCloseTimeRequest",
    "GetConsumptionRequest",
    "GetCurrentBillRequest",
    "GetCurrentSittingStateRequest",
    "GetCurrentTemperatureRequest",
    "GetDetectedTimeRequest",
    "GetDetectionCountRequest",
    "GetDeviceStateRequest",
    "GetEstimateBillRequest",
    "GetEstimateConsumptionRequest",
    "GetExpendableStateRequest",
    "GetFineDustRequest",
    "GetHealthScoreRequest",
    "GetHumidityRequest",
    "GetKeepWarmTimeRequest",
    "GetLockStateRequest",
    "GetMuscleRequest",
    "GetNoticeRequest",
    "GetOpenStateRequest",
    "GetOpenTimeRequest",
    "GetPackageRequest",
    "GetPhaseRequest",
    "GetPowerStateRequest",
    "GetProgressiveTaxBracketRequest",
    "GetRemainingTimeRequest",
    "GetRightPostureRatioRequest",
    "GetSleepScoreRequest",
    "GetSleepStartTimeRequest",
    "GetTargetTemperatureRequest",
    "GetUltraFineDustRequest",
    "GetUsageTimeRequest",
    "GetVehicleLocationRequest",
    "GetWeightRequest",
    "HealthCheckRequest",
]

INTERFACE_CONTROL = (
    INTERFACE_VALUE_SETTING + 
    INTERFACE_INCREMENTAL +
    INTERFACE_SWITCHING +
    INTERFACE_ACTION +
    INTERFACE_GET
)

ACTION = namedtuple("ACTION", "name request response domain prefix suffix")
ACTIONS = { 
    y[0]: ACTION(
        y[0], 
        '{}{}'.format(y[0],SUFFIX_REQUEST), 
        '{}{}'.format(y[0],SUFFIX_RESPONSE if "{}{}".format(y[0], SUFFIX_REQUEST) in INTERFACE_GET else SUFFIX_CONFIRMATION), 
        x.domain,
        y[1],
        y[2]
    ) 
    for x in _ACTIONS
    for y in [
        ('{}{}{}'.format(_, x.name, __), _, __)
        for _ in (x.prefix if x.prefix else [""])
        for __ in (x.suffix if x.suffix else [""])
    ]
}

HVAC_MODES =  {
    "auto": HVAC_MODE_AUTO,
    "cool":  HVAC_MODE_COOL,
    "dehumidify": HVAC_MODE_DRY, 
    "fan": HVAC_MODE_FAN_ONLY, 
    "heat": HVAC_MODE_HEAT, 
    "powercool": "", 
    "powersaving": "", 
    "sleep": ""
}

FAN_MODES = {

    climate.DOMAIN : 
    {
        1: FAN_LOW,
        2: FAN_MEDIUM,
        3: FAN_HIGH,
    },

    fan.DOMAIN : 
    {
        1: fan.SPEED_LOW,
        2: fan.SPEED_MEDIUM,
        3: fan.SPEED_HIGH,
    }
}

SWING_MODES = {
    "horizontal": SWING_HORIZONTAL,
    "vertical": SWING_VERTICAL
}

PRESET_MODES = {
    "auto": fan._NOT_SPEED_AUTO,
    "baby": fan._NOT_SPEED_SILENT,
    "sleep": fan._NOT_SPEED_SLEEP
}