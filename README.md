# 클로바홈EX for HA

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.4][version-shield]

CLOVA Home extension 컴포넌트 입니다.
CEK를 통해 CLOVA와 홈어시스턴트 사이의 커뮤니케이션을 지원합니다.

### Version history
| 버전     | 일자        | 내용              |
| :-----: | :---------: | ----------------------- |
| **v1.1.0**  | 2021.11.06  | - 메뉴얼 추가<br>- 스키마 파일(`schema.py`) 추가 <br>- 디바이스 설정 추가<br>- 액션 설정 추가 |
| **v1.0.2**  | 2021.11.01  | - 오류 수정 <br>- `FAN` 도메인에 대한 모든 액션 추가  |
| **v1.0.1**  | 2021.10.31  | String.json 파일과 translations 폴더 삭제  |
| **v1.0.0**  | 2021.10.31  | First version  |

### Update log

> 초기 버전보다 많은 기능이 업데이트 되었습니다.

1. **메뉴얼을 작성했습니다.**<br>
설정가능한 변수가 많이 추가되어 따로 메뉴얼을 작성했습니다.

2. **스키마 파일을 따로 작성하여 유효성 검사를 강화했습니다.**<br>
`configuration.yaml`을 작성하고 서버를 재시작하기전에 유효성 검사를 통해 설정파일이 잘 작성되었는지 확인하여 재로딩 시간을 줄일 수 있습니다.
`response`도 유효성 검사를 적용하려했지만 템플릿 언어를 적용했다는 사실을 잊은채 스키마를 작성하여 유효성 검사를 통과하지 못하여 이번 버전에서는 적용하지 않았습니다..

3. **디바이스 설정을 자유롭게 할 수 있습니다.**<br>
디바이스 이름이나 제조사, 태그 등을 자유롭게 변경할 수 있습니다. 클로바 서버에서 인식하는 디바이스 타입도 설정할 수 있습니다.

4. **커스텀 액션을 수행할 수 있습니다.**<br>
디바이스의 `actionDetails`를 설정하여 다른 서비스를 실행하고 사용자가 지정한 응답 메시지를 반환하도록 할 수 있습니다. 클로바의 디바이스 타입이 세세하게 나눠져 있어서 홈어시스턴트의 도메인에 매칭되는 타입이 제한됩니다. 이때 `actionDetails`를 설정하여 액션마다 실행하는 서비스를 지정할 수 있고 사용자가 작성한 응답 메시지를 반환할 수 있습니다.(응답 메시지는 타입별로 형태가 정해져있습니다.)

### 후원

**카카오 페이** <br>
![후원](https://github.com/huimang2/clova_ex/blob/main/images/KakaoPay_QR.png)

-----
# 1. 컴포넌트 설치

### Manual

- HA 설치 경로 아래 custom_components에 clova폴더 안의 전체 파일을 복사해줍니다.<br>
  `<config directory>/custom_components/clova/`<br>
- Home-Assistant 를 재시작합니다<br>

<br>

### HACS
- HACS > Integretions > 우측상단 메뉴 > Custom repositories 선택
- 'https://github.com/huimang2/clova' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, '[KR] 클로바홈EX' 검색하여 설치

<br>

# 2. CLOVA Home extension 등록

> **참고** 
> * 아래 페이지를 참고하여 CLOVA Home extension을 등록하세요.
https://developers.naver.com/console/clova/home_ext/DevConsole/Guides/Register_Clova_Home_Extension.md
>
> * HA 도메인은 SSL 인증서를 사용하여 외부에서 Home Assistnat에 접근 가능해야 합니다.
>
> * 심사신청은 하지마세요!

**1) [CLOVA Developers Consor β](https://developers.naver.com/console/clova/cek/#/list)에 접속하여 `CLOVA Home extension 만들기`를 클릭하세요.** 

**2) 서버 설정은 다음과 같이 입력합니다.** <br>

> - **Extension 서버 URL**: `https://HA주소/api/clova`
> - **로그인 URL**: `https://HA주소/auth/authorize`
> - **클라이언트ID**: `https://prod-ni-cic.clova.ai/`
> - **Access token URI**: `https://HA주소/auth/token?grant_type=authorization_code`
> - **Access token 재발급 URI (선택)**: `https://HA주소/auth/token?>grant_type=refresh_token`
> - **클라이언트 secret**: `아무 글자나 입력`

![캡쳐1](https://github.com/huimang2/clova_ex/blob/main/images/capture-001.png)

**3) 로고는 `250 * 250` 사이즈의 이미지, 배너는 `750 * 500` 사이즈의 이미지를 사용합니다.** <br>
![캡쳐2](https://github.com/huimang2/clova_ex/blob/main/images/capture-002.png)<br>
![로고](https://github.com/huimang2/clova_ex/blob/main/images/logo.png)<br>
![배너](https://github.com/huimang2/clova_ex/blob/main/images/banner.png)

# 3. 클로바에 컴포넌트 연결

**1) 클로바 어플리케이션 다운로드 후 실행** 

**2) 하단에 위치한 `스마트홈 아이콘` 클릭** <br>
![캡쳐3](https://github.com/huimang2/clova_ex/blob/main/images/capture-003.png)

**3) `+ 기기 추가하기` 클릭** <br>
![캡쳐4](https://github.com/huimang2/clova_ex/blob/main/images/capture-004.png)

**4) 추가한 `extension` 클릭** <br>
![캡쳐5](https://github.com/huimang2/clova_ex/blob/main/images/capture-005.png)

**5) `로그인`을 클릭하여 홈어시스턴트 아이디로 로그인** <br>
![캡쳐6](https://github.com/huimang2/clova_ex/blob/main/images/capture-006.png)

**6) 연동된 기기 확인** <br>
![캡쳐7](https://github.com/huimang2/clova_ex/blob/main/images/capture-007.png)

# 4. `configuration.yaml` 설정

클로바홈EX를 실행시키기 위해서는 `configuration.yaml` 파일을 설정해야 합니다.

``` YAML
clova:

```

## 기본 설정 변수

#### `configuration.yaml` 작성 예시
``` YAML
clova:
  expose_by_default: False
  exposed_domains:
    - switch
    - climate
  customCommands: []
  entity_config: ...
```

| 변수 | 자료형 | 필수/선택 | 설명 |
| :--: | :--: | :------: |---- |
| **expose_by_default** | *Boolean* | 선택 | 기본값은 **`True`** 이며지원되는 모든 디바이스를 노출합니다.<br>**`False`** 로 설정하면 수동으로 `expose`를 설정해야합니다.
| **exposed_domains** | *list* [] | 선택 | 노출을 허용하는 도메인을 설정합니다. 기본값은 다음과 같습니다.<br>- climate<br>- cover<br>- fan<br>- group<br>- humidifier<br>- light<br>- lock<br>- media_player<br>- switch<br>- vacuum
| **customCommands** | *dict array*<br>[dict] | 선택 | 커스텀 커맨드를 설정합니다.(미구현)
| **entity_config** | *dict* | 선택 | 구성요소를 설정합니다.

## `customCommands` 설정

> 참고 : 클로바 서버에 값을 전달해도 해당 명령어가 내 명령어에 표시되지 않습니다.<br>
> 아직 **미구현** 상태입니다.

#### `configuration.yaml` 작성 예시
``` YAML
clova:
  customCommands:
    - name: "외출모드"
      actions:
        - entity_id: switch.geosil_jeondeung
          action: TurnOff
        - entity_id: switch.jubang_jeondeung
          action: TurnOff
        - entity_id: switch.keunbang_jeondeung
          action: TurnOff
```

## `entity_config` 구성

> 참고 : `entity_config`를 설정하여 각각의 디바이스마다 커스텀화가 가능합니다.

#### `configuration.yaml` 작성 예시
``` YAML
clova:
  expose_by_default: false
  entity_config:
    switch.geosil_jeondeung:
      expose: true
      name: 거실 전등
      manufacturer: 삼성
      model: 2021년형
      version: v1.1
      description: 2021년형 삼성 LED 등입니다.
      type: SWITCH
      ir: false
      location: LIVING_ROOM
      tag: [거실]
      actionDetails: ...
```

| 변수 | 자료형 | 필수/선택 | 설명 |
| :--: | :--: | :------: |---- |
| **expose** | *Boolean* | 선택 | 구성요소별로 노출여부를 설정합니다. 기본값은 **`True`** 입니다.
| **name** | *str* | 선택 | 클로바에 명시되는 디바이스명 입니다.
| **manufacturer** | *str* | 선택 | 클로바에 명시되는 제조사명 입니다.
| **model** | *str* | 선택 | 클로바에 명시되는 모델명 입니다.
| **version** | *str* | 선택 | 클로바에 명시되는 버전 입니다.
| **description** | *str* | 선택 | 클로바에 명시되는 디바이스 설명 입니다.
| **type** | *str* | 선택 | 클로바에서 인식하는 지정된 디바이스 타입으로 변경합니다.
| **ir** | *str* | 선택 | 디바이스가 적외선 기능을 사용하는지를 나타냅니다. 기본값은 **`False`**입니다.
| **location** | *str* | 선택 | 클로바에서 인식하는 지정된 장소명 입니다.
| **tags** | *list* [] | 선택 | 클로바에서 설정하는 그룹명 입니다. 여러 그룹을 설정 가능합니다.
| **actionDetails** | *dict array*<br>[dict] | 선택 | 구성요소의 액션에 대한 세부사항을 설정합니다.

## `type` 변수

`type` 값은 지정된 디바이스 타입을 입력해야 합니다. 디바이스 타입마다 사용할 수 있는 액션이 정해져 있습니다. 소문자로 입력해도 대문자로 변환되어 전달됩니다.

| 타입 | 허용되는 액션 |
| :--: |------------ |
| **AIRCONDITIONER**<br>(에어컨 타입) | ChangeFanSpeed, ChangeMode, ChangePower, DecrementFanSpeed, DecrementTargetTemperature, GetCurrentTemperature, GetDeviceState, GetTargetTemperature, HealthCheck, IncrementFanSpeed, IncrementTargetTemperature, SetFanSpeed, SetMode, SetTargetTemperature, StartOscillation, StopOscillation, TurnOff, TurnOn |
| **AIRPURIFIER**<br>(공기청정기 타입) | ChangeFanSpeed, ChangeMode, ChangePower, DecrementFanSpeed, GetAirQuality, GetCurrentTemperature, GetDeviceState, GetFineDust, GetHumidity, GetUltraFineDust, HealthCheck, IncrementFanSpeed, ReleaseMode, SetFanSpeed, SetMode, TurnOff, TurnOn |
| **AIRSENSOR**<br>(공기질 측정기 타입) | GetAirQuality, GetCurrentTemperature, GetDeviceState, GetFineDust, GetHumidity, GetUltraFineDust, HealthCheck |
| **BIDET**<br>(비데 타입) | Close, GetDeviceState, GetExpendableState, HealthCheck, Open, TurnOff, TurnOn |
| **BODYWEIGHTSCALE**<br>(체중계 타입) | GetBMI, GetBatteryInfo, GetDeviceState, GetBodyFat, GetHealthScore, GetMuscle, GetWeight, HealthCheck |
| **BUILDING_ELECTRIC_METER**<br>(아파트 전기 타입) | GetConsumption |
| **BUILDING_ELEVATOR_CALLER**<br>(아파트 엘리베이터 타입) | CallElevator |
| **BUILDING_GAS_METER**<br>(아파트 가스 타입) | GetConsumption |
| **BUILDING_HEATING_METER**<br>(아파트 난방 타입) | GetConsumption |
| **BUILDING_HOTWATER_METER**<br>(아파트 온수 타입) | GetConsumption |
| **BUILDING_NOTICE_MONITOR**<br>(아파트 공지사항 타입) | GetNotice |
| **BUILDING_PACKAGE**<br>(아파트 택배 타입) | GetPackage |
| **BUILDING_PARKING_MONITOR**<br>(아파트 주차 타입) | GetVehicleLocation |
| **BUILDING_UTILITY_BILL_MONITOR**<br>(아파트 관리비 타입) | GetCurrentBill |
| **BUILDING_WATER_METER**<br>(아파트 수도 타입) | GetConsumption |
| **CLOTHESCAREMACHINE**<br>(의류 관리기 타입) | GetDeviceState, GetPhase, GetRemainingTime, HealthCheck, TurnOff, TurnOn |
| **CLOTHESDRYER**<br>(의류 건조기 타입) | GetDeviceState, GetPhase, GetRemainingTime, HealthCheck, TurnOff, TurnOn |
| **CLOTHESWASHER**<br>(의류 세탁기 타입) | GetDeviceState, GetPhase, GetRemainingTime, HealthCheck, TurnOff, TurnOn |
| **DEHUMIDIFIER**<br>(제습기 타입) | GetCurrentTemperature, GetDeviceState, GetHumidity, HealthCheck, SetFanSpeed, TurnOff, TurnOn |
| **DISHWASHER**<br>(식기 세척기 타입) | GetDeviceState, GetPhase, GetRemainingTime, HealthCheck, TurnOff, TurnOn |
| **ELECTRICKETTLE**<br>(전기 주전자 타입) | GetCurrentTemperature, GetDeviceState, HealthCheck, TurnOff, TurnOn |
| **ELECTRICTOOTHBRUSH**<br>(전동 칫솔 타입) | GetDeviceState, HealthCheck |
| **FAN**<br>(선풍기 타입) | DecrementFanSpeed, GetDeviceState, HealthCheck, IncrementFanSpeed, SetFanSpeed, SetMode, StartOscillation, StopOscillation, TurnOff, TurnOn |
| **HEATER**<br>(히터 타입) | DecrementTargetTemperature, GetCurrentTemperature, GetDeviceState, GetTargetTemperature, HealthCheck, IncrementTargetTemperature, SetTargetTemperature, TurnOff, TurnOn |
| **HOMECAM**<br>(홈캠 타입) | GetDetectionCount, HealthCheck, ReleaseMode, SetMode, StartRecording, StopRecording, TurnOff, TurnOn |
| **HUMIDIFIER**<br>(가습기 타입) | GetCurrentTemperature, GetDeviceState, GetHumidity, HealthCheck, ReleaseMode, SetFanSpeed, SetMode, TurnOff, TurnOn |
| **KIMCHIREFRIGERATOR**<br>(김치 냉장고 타입) | GetDeviceState, HealthCheck |
| **LIGHT**<br>(스마트 조명 기기 타입) | DecrementBrightness, DecrementVolume HealthCheck, GetDeviceState, IncrementBrightness, IncrementVolume, ReleaseMode, SetBrightness, SetColor, SetColorTemperature, SetMode, TurnOff, TurnOn |
| **MASSAGECHAIR**<br>(안마 의자 타입) | DecrementIntensityLevel, GetDeviceState, HealthCheck, IncrementIntensityLevel, TurnOff, TurnOn |
| **MICROWAVE**<br>(전자 레인지 타입) | GetDeviceState, GetRemainingTime, HealthCheck, TurnOff, TurnOn |
| **MOTIONSENSOR**<br>(동작 감지 센서 타입) | GetDetectedTime, GetDeviceState, GetPowerState, HealthCheck, ReleaseMode, SetMode, TurnOff, TurnOn |
| **OPENCLOSESENSOR**<br>(열림 감지 센서 타입) | GetCloseTime, GetDeviceState, GetOpenState, GetOpenTime, HealthCheck |
| **OVEN**<br>(오븐 타입) | GetDeviceState, GetRemainingTime, HealthCheck, Preheat |
| **POWERSTRIP**<br>(멀티 탭 타입) | GetConsumption, GetDeviceState, GetEstimateBill, GetProgressiveTaxBracket, HealthCheck, TurnOff, TurnOn |
| **PURIFIER**<br>(정수기 타입) | GetConsumption, GetDeviceState, GetExpendableState, HealthCheck, ReleaseMode, SetMode, SetTargetTemperature |
| **RANGE**<br>(레인지 타입) | GetDeviceState, HealthCheck |
| **RANGEHOOD**<br>(레인지 후드 타입) | GetDeviceState, HealthCheck, TurnOff, TurnOn |
| **REFRIGERATOR**<br>(냉장고 타입) | GetDeviceState, HealthCheck, ReleaseMode, SetMode, SetTargetTemperature |
| **RICECOOKER**<br>(전기 밥솥 타입) | GetCleaningCycle, GetDeviceState, GetExpendableState, GetKeepWarmTime, GetPhase, GetRemainingTime, HealthCheck, ReleaseMode, SetMode, Stop, TurnOff, TurnOn |
| **ROBOTVACUUM**<br>(로봇 청소기 타입) | Charge, GetBatteryInfo, GetDeviceState, HealthCheck, TurnOff, TurnOn |
| **SETTOPBOX**<br>(TV 셋톱 박스 타입) | ChangeInputSource, ChangePower, DecrementChannel, DecrementVolume, GetDeviceState, HealthCheck, IncrementChannel, IncrementVolume, Mute, SetChannel, SetChannelByName, TurnOff, TurnOn, Unmute |
| **SLEEPINGMONITOR**<br>(수면 센서 타입) | GetAsleepDuration, GetAwakeDuration, GetDeviceState, GetSleepScore, GetSleepStartTime, HealthCheck, TurnOff, TurnOn |
| **SMARTBED**<br>(스마트 침대 타입) | GetDeviceState, HealthCheck, Lower, Raise, Stop |
| **SMARTCHAIR**<br>(스마트 의자 타입) | GetCurrentSittingState, GetDeviceState, GetRightPostureRatio, GetUsageTime, HealthCheck |
| **SMARTCURTAIN**<br>(스마트 커튼 타입) | Close, GetDeviceState, HealthCheck, Open, Stop |
| **SMARTHUB**<br>(스마트 허브 타입) | GetCurrentTemperature, GetDeviceState, GetHumidity, GetTargetTemperature, HealthCheck, SetMode |
| **SMARTLOCK**<br>(스마트락(도어락) 타입) | GetDeviceState, GetLockState, HealthCheck, SetLockState |
| **SMARTMETER**<br>(전기 계량기 타입) | GetConsumption, GetCurrentBill, GetDeviceState, GetEstimateBill, GetProgressiveTaxBracket, HealthCheck |
| **SMARTPLUG**<br>(스마트 플러그 타입) | GetConsumption, GetDeviceState, GetEstimateBill, HealthCheck, TurnOff, TurnOn |
| **SMARTTV**<br>(스마트 TV 타입) | ChangeInputSource, ChangePower, DecrementChannel, DecrementVolume, GetDeviceState, HealthCheck, IncrementChannel, IncrementVolume, Mute, SetChannel, SetChannelByName, TurnOff, TurnOn, Unmute |
| **SMARTVALVE**<br>(스마트 밸브 타입) | GetDeviceState, GetLockState, SetLockState |
| **SMOKESENSOR**<br>(연기 센서 타입) | GetDeviceState, HealthCheck |
| **SWITCH**<br>(가정 내 콘센트 전원을 제어하는 스위치 타입) | GetDeviceState, HealthCheck, TurnOff, TurnOn |
| **THERMOSTAT**<br>(온도 조절 기기 타입) | DecrementTargetTemperature, GetConsumption, GetCurrentTemperature, GetDeviceState, GetEstimateConsumption, GetTargetTemperature, HealthCheck, IncrementTargetTemperature, SetMode, SetTargetTemperature TurnOff, TurnOn |
| **VENTILATOR**<br>(환풍기 타입) | GetAirQuality, GetCurrentTemperature, GetDeviceState, GetHumidity, GetTargetTemperature, HealthCheck, ReleaseMode, SetFanSpeed, SetMode, TurnOff, TurnOn |
| **WATERBOILER**<br>(온수기 타입) | GetDeviceState, HealthCheck, SetMode, TurnOff, TurnOn |
| **WINECELLAR**<br>(와인 셀러 타입) | GetDeviceState, HealthCheck, ReleaseMode, SetMode, SetTargetTemperature, TurnOff, TurnOn |

> 홈어시스턴트의 도메인은 다음과 같은 타입으로 변환됩니다.

| 도메인 | 타입 | 구현 여부 |
| :---: | :--: | :------: |
| **switch** | SWITCH | O |
| **climate** | AIRCONDITIONER | O |
| **fan** | FAN | O |
| **cover** | SMARTCURTAIN | X |
| **group** | SWITCH | O |
| **light** | LIGHT | X |
| **lock** | SMARTLOCK | X |
| **media_player** | SETTOPBOX | X |
| **vacuum** | ROBOTVACUUM | X |
| **camera** | TYPE_HOMECAM | X |
| **binary_sensor**<br>(opening 클래스) | OPENCLOSESENSOR | X |
| **binary_sensor**<br>(window 클래스) | OPENCLOSESENSOR | X |
| **media_player**<br>(TV 클래스) | SMARTTV | X |
| **humidifier**<br>(humidifier 클래스) | HUMIDIFIER | X |
| **humidifier**<br>(dehumidifier 클래스) | DEHUMIDIFIER | X |

> 참고 : 완전히 구현된 도메인은 switch, climate, fan, group 입니다.<br>
> 나머지 도메인은 기본적인 ON/OFF 액션만 구현된 상태입니다.

## `location` 변수

`location` 값은 지정된 장소 타입을 입력해야 합니다. 해당 장소 타입은 지정된 그룹으로 편성됩니다.
`tags` 변수를 통해서도 그룹 지정이 가능하므로 값이 지정된 `location` 보다는 `tags`를 사용하는 것이 더 편합니다.

| 타입 | 그룹 |
| :--: | :--: |
| **ATTIC** | 다락방 |
| **BALCONY** | 베란다 |
| **BALCONY_IN_LIVING_ROOM** | 거실베란다 |
| **BALCONY_IN_MAIN_ROOM** | 안방베란다 |
| **BALCONY_KITCHEN** | 주방베란다 |
| **BATH_ROOM** | 화장실 |
| **BATH_ROOM_IN_LIVING_ROOM** | 거실 화장실 |
| **BATH_ROOM_IN_MAIN_ROOM** | 안방 화장실 |
| **BED_ROOM** | 침실 |
| **BIG_BATH_ROOM** | 큰 화장실 |
| **BIG_CHILD_ROOM** | 큰아이 방 |
| **BIG_ROOM** | 큰 방 |
| **BOILER_ROOM** | 보일러실 |
| **DINING_ROOM** | 식당 |
| **DRESS_ROOM** | 드레스룸 |
| **ENTRANCE** | 현관 |
| **FAMILY_ROOM** | 가족룸 |
| **FATHER_ROOM** | 아버님방 |
| **FIFTH_ROOM** | 다섯째 방 |
| **FIRST_ROOM** | 첫째 방 |
| **FOURTH_ROOM** | 넷째 방 |
| **HALLWAY** | 복도 |
| **KITCHEN** | 주방 |
| **LIBRARY** | 서재 |
| **LIVING_ROOM** | 거실 |
| **MAIN_GATE** | 대문 |
| **MAIN_ROOM** | 안방 |
| **MOTHER_ROOM** | 어머님방 |
| **MY_ROOM** | 내 방 |
| **PARENTS_ROOM** | 부모님 방 |
| **PLAY_ROOM** | 놀이방 |
| **POWDER_ROOM** | 파우더룸 |
| **ROOM** | 방 |
| **SECOND_ROOM** | 둘째 방 |
| **SMALL_CHILD_ROOM** | 작은아이 방 |
| **SMALL_LIVING_ROOM** | 작은 거실 |
| **SMALL_ROOM** | 작은 방 |
| **SMALL_KITCHEN** | 작은 주방 |
| **SMALL_BATH_ROOM** | 작은 화장실 |
| **STAIRS** | 계단 |
| **THIRD_ROOM** | 셋째 방 |
| **UPSTAIRS_ROOM** | 윗층 방 |
| **UTILITY_ROOM** | 다용도실 |
| **WAREHOUSE** | 창고 |
| **YARD** | 마당 |

## `actionDetails` 구성

`actionDetails`을 설정하여 사용자가 지정한 서비스를 불러오는 것이 가능합니다.
또한 `allowableValue`를 설정하여 클로바 서버로 해당 액션이 허용하는 값을 전달할 수 있습니다.

액션명은 [클로바 플랫폼 가이드](https://developers.naver.com/console/clova/home_ext/Develop/References/ClovaHomeInterface/Shared_Objects.md#Actions)를 참고하세요.

#### JSON 형식
``` JSON
"actionDetails": {
  "액션명": {
    "service": "domain.service",
    "data": dict,
    "response": dict,
    "allowableValue": {
      "type": "타입",
      "minValue": int,
      "maxValue": int,
      "enumValues": list
    }
  }
}
```

#### `configuration.yaml` 작성 예시
``` YAML
clova:
  entity_config:
    switch.geosil_jeondeung:
      actionDetails:
        TurnOn:
          service: input_text.set_value
          data:
            entity_id: input_text.test
            value: {{ states("switch.geosil_jeondeung") }} 상태
```
`switch.geosil_jeondeung`으로 `TurnOn` 액션 요청이 오면 `input_text` 도메인의 `set_value` 서비스를 실행하여 `input_text.test` 구성요소에 `switch.geosil_jeondeung` 구성요소의 의 상태를 기록하게 됩니다.

> 참고 : 홈어시스턴트의 템플릿 언어를 사용하여 데이터를 전달할 수 있습니다.

| 변수 | 자료형 | 필수/선택 | 설명 |
| :--: | :---: | :------: |----- |
| **action** | dict | 필수 | 해당 dictionary의 키값으로 `action`을 사용합니다. <br>`actionDetails`을 설정하면 필수로 입력해야하며 해당 구성요소가 수행할 수 있는 액션만 입력가능합니다. <br>위의 예시에서는 `switch` 도메인에서 `TurnOn` 액션을 설정했으며, `switch` 도메인은 `SWITCH` 타입에 해당하여 해당 액션을 사용가능합니다.|
| **service** | service_id | 선택 | 액션에 요청이 오면 해당 서비스를 수행합니다. |
| **data** | dict | 선택 | 서비스의 payload 입니다. 서비스와 함께 작동합니다. |
| **response** | dict | 필수 | 클로바 서버의 요청에 대한 응답을 설정합니다. 기본값은 {}이며, 응답 메시지의 형식은 [클로바 개발문서](https://developers.naver.com/console/clova/home_ext/Develop/References/Message_Interfaces.md)를 참고하세요. Response 메시지의 `payload` 부분만 작성하면 됩니다. |
| **allowableValue** | dict | 선택 | 액션의 허용값을 설정합니다.<br>`type`은 **[string, number, boundedNumber]** 중에 하나를 입력합니다.<br>`minValue`와 `maxValue`는 `type`이 **"boundedNumber"** 인 경우 필수로 입력해야합니다.<br>`enumValues`는 `type`이 **"string"** 이면 문자열 배열, `type`이 **"number"** 이면 숫자 배열을 입력합니다. |

## Request값 이용하기

> Request값은 자체적인 문법을 사용합니다. **`@경로@`** 형식으로 입력합니다.
>
> 경로는 payload 아래 경로를 입력합니다.

예를들어

``` JSON
{
  "header": {
    "messageId": "33da6561-0149-4532-a30b-e0de8f75c4cf",
    "name": "SetModeRequest",
    "namespace": "ClovaHome",
    "payloadVersion": "1.0"
  },
  "payload": {
    "accessToken": "92ebcb67fe33",
    "appliance": {
        "applianceId": "device-006"
    },
    "mode": {
        "value": "hotwater"
    }
  }
}
```

다음과 같은 형식의 요청이 들어오고 `mode`의 `value`값을 이용하고 싶다면 **`@mode.value@`** 라고 입력하면 됩니다.

#### 예시

``` YAML
clova:
  expose_by_default: false
  entity_config:
    input_text.test:
      expose: true
      type: RICECOOKER
      actionDetails:
        SetMode:
          service: input_text.set_value
          data:
            entity_id: input_text.test
            value: "@mode.value@"
          response:
            mode:
              value: "@mode.value@"
```

`input_text.test` 구성요소를 만들고 다음과 같이 작성하면 밥솥에 대한 SetMode 액션을 실행할 수 있습니다.

![캡쳐9](https://github.com/huimang2/clova_ex/blob/main/images/capture-009.png)

![캡쳐10](https://github.com/huimang2/clova_ex/blob/main/images/capture-010.png)

## 예시

#### 전력 측정기 설정
``` YAML
clova:
  expose_by_default: false
  entity_config:
    sensor.electricity_monitor_energy:
      expose: true
      type: building_electric_meter
      actionDetails:
        GetConsumption:
          response:
            - name: 전기사용량
              value: "{{ states('sensor.electricity_monitor_energy') | int }}"
              unit: KW

```

![캡쳐8](https://github.com/huimang2/clova_ex/blob/main/images/capture-008.png)

# 참고

- 네이버 카페 : HomeAssistant (https://cafe.naver.com/koreassistant)
- 클로바 플랫폼 가이드 (https://developers.naver.com/console/clova/home_ext/)

[version-shield]: https://img.shields.io/badge/version-v1.1.0-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
