# 클로바홈EX for HA

![HAKC)][hakc-shield]
![HACS][hacs-shield]
![Version v1.4][version-shield]

CLOVA Home extension 컴포넌트 입니다. <br>
CEK를 통해 CLOVA와 홈어시스턴트 사이의 커뮤니케이션을 지원합니다. <br>

<br>

## Version history
| Version | Date        | 내용              |
| :-----: | :---------: | ----------------------- |
| v1.0.0  | 2021.10.31  | First version  |
| v1.0.1  | 2021.10.31  | String.json 파일과 translations 폴더 삭제  |
| v1.0.2  | 2021.11.01  | - 오류 수정 <br>- `FAN` 도메인에 대한 액션 모두 추가  |

<br>

## Installation
### Manual
- HA 설치 경로 아래 custom_components에 clova폴더 안의 전체 파일을 복사해줍니다.<br>
  `<config directory>/custom_components/clova/`<br>
- Home-Assistant 를 재시작합니다<br>
### HACS
- HACS > Integretions > 우측상단 메뉴 > Custom repositories 선택
- 'https://github.com/huimang2/clova' 주소 입력, Category에 'integration' 선택 후, 저장
- HACS > Integretions 메뉴 선택 후, '[KR] 클로바홈EX' 검색하여 설치

<br>

## Usage
### CLOVA Home extension 등록하기

* 아래 페이지를 참고하여 CLOVA Home extension을 등록하세요.
https://developers.naver.com/console/clova/home_ext/DevConsole/Guides/Register_Clova_Home_Extension.md

* HA 도메인은 SSL 인증서를 사용하여 외부에서 Home Assistnat에 접근 가능해야 합니다.

* extension을 만들때 서버 부분은 다음과 같이 입력합니다.
  - **Extension 서버 URL**: `https://HA주소/api/clova`
  - **로그인 URL**: `https://HA주소/auth/authorize`
  - **클라이언트ID**: `https://prod-ni-cic.clova.ai/`
  - **Access token URI**: `https://HA주소/auth/token?grant_type=authorization_code`
  - **Access token 재발급 URI (선택)**: `https://HA주소/auth/token?grant_type=refresh_token`
  - **클라이언트 secret**: `아무 글자나 입력`
* 심사신청은 하지마세요!
 
[version-shield]: https://img.shields.io/badge/version-v1.0.1-orange.svg
[hakc-shield]: https://img.shields.io/badge/HAKC-Enjoy-blue.svg
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-red.svg
