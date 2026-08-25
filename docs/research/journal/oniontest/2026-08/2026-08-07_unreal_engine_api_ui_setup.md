# 2026-08-07 Onion Test Unreal Engine API·UI 구조 작업

## 오늘의 목표

모델 비교가 끝날 때까지 Unreal 작업을 미루지 않고, ONN-C와 MND-N의 결과를 Unreal Engine에서 받을 수 있는 첫 수직 흐름을 준비했다. 오늘은 실제 HTTP Event Graph를 완성하기보다 프로젝트 연결을 검증하고 `WBP_OnionChat`의 UI 구조를 만드는 데 범위를 제한했다.

```text
사용자 입력
-> Unreal Http Blueprint
-> ONN-C POST /v1/conversations/respond
-> onn-c.v1 JSON 응답
-> 대사·상태·애니메이션 키 표시
```

## 작업 환경

- Unreal 프로젝트: `C:\Discovery\Cosmo\dev\maam-mini-game\oniontest\oniontest`
- Unreal Engine: 5.8
- ONN-C API: `http://127.0.0.1:8765`
- API Schema: `onn-c.v1`
- Widget Blueprint: `/Game/Onion/UI/WBP_OnionChat`
- 캐릭터 Blueprint: `/Game/Onion/Blueprints/BP_OnionPlaceable`
- Onion 애니메이션: 24개

## Codex와 Unreal의 연결 방식

Codex는 Unreal 프로젝트의 설정·스크립트·코드를 수정하고 Unreal Editor를 명령행으로 실행해 로그와 에셋을 검증한다. `.uasset`의 Blueprint Graph를 텍스트처럼 직접 수정하지 않고, Unreal Python으로 에셋을 확인하거나 사용자가 에디터에서 노드를 연결하는 방식을 사용한다.

연결은 두 층으로 구분한다.

1. 에디터 자동화: `PythonScriptPlugin`과 `Scripts/*.py`
2. 게임 실행 중 통신: UE 5.8 기본 `HttpBlueprint`와 `JsonBlueprintUtilities`

처음에는 C++ `OnionBridge` 런타임 플러그인을 검토했으나 PC에 Visual Studio와 Windows SDK `10.0.19041.0`이 없어 컴파일할 수 없었다. UE 5.8에 HTTP·JSON Blueprint 플러그인이 기본 포함된 것을 확인하고, 별도 C++ 빌드 없이 진행하는 방향으로 변경했다.

## 자동 검증 결과

`Scripts/verify_onion_api_bridge.py`를 Unreal Editor 커맨드 모드에서 실행해 다음 항목을 확인했다.

| 검증 항목 | 결과 |
|---|---|
| Unreal Engine | 5.8.0 |
| HttpBlueprint 로드 | 성공 |
| JsonBlueprintUtilities 로드 | 성공 |
| ONN-C `/health` | `ok` |
| API Schema | `onn-c.v1` |
| Onion 캐릭터 에셋 | 확인 |
| BP_OnionPlaceable | 확인 |
| Onion 애니메이션 | 24개 확인 |

검증 결과는 Unreal 프로젝트의 `Saved/OnionApiBridgeVerification.json`에 로컬로 생성된다. `Saved` 폴더는 Git에 올리지 않는다.

## UMG 용어 복습

| 한글 설명 | Unreal 용어 | 의미 |
|---|---|---|
| 화면 기준점 | 앵커(Anchor) | 화면 크기가 바뀔 때 위젯 위치를 계산하는 기준 |
| 기준점에서의 거리·여백 | 오프셋(Offset) | Anchor를 기준으로 위치 또는 가장자리 여백 조절 |
| 내부 여백 | 패딩(Padding) | 컨테이너 안에서 자식 위젯과 경계 사이의 간격 |
| 안전 영역 | 안전 영역(Safe Zone) | 노치와 시스템 UI를 피해 콘텐츠를 배치하는 영역 |
| 세로 컨테이너 | 세로 상자(Vertical Box) | 자식 위젯을 위에서 아래로 정렬 |
| 가로 컨테이너 | 가로 상자(Horizontal Box) | 자식 위젯을 왼쪽에서 오른쪽으로 정렬 |

이번 Widget에서는 `Safe Zone`이 최상위 위젯이므로 `Canvas Panel Slot`, Anchor와 Offset이 표시되지 않는 것이 정상이다. 최상위 Safe Zone은 이미 전체 화면을 차지하고, 자식 `Vertical Box`의 Safe Zone Slot에서 정렬과 Padding을 설정한다.

## 오늘 만든 UI 구조

```text
WBP_OnionChat
└─ SafeZone_28
   └─ Panel_Chat
      ├─ Text_Status
      ├─ SizeBox_Response
      │  └─ ScrollBox_Response
      │     └─ Text_Response
      ├─ Spacer_Vertical
      └─ HorizontalBox_Input
         ├─ Input_Message
         ├─ Spacer_Horizontal
         └─ SizeBox_Send
            └─ Button_Send
               └─ Text_Send
```

`Panel_Chat`의 Safe Zone Slot 설정은 다음과 같다.

- 가로 정렬(Horizontal Alignment): 채우기(Fill)
- 세로 정렬(Vertical Alignment): 아래쪽(Bottom)
- 패딩(Padding): 상하좌우 32

주요 위젯 설정:

- `Text_Status`: 기본값 `Ready`, 변수 활성화
- `SizeBox_Response`: 높이 200
- `Text_Response`: 자동 줄바꿈, 변수 활성화
- `Input_Message`: 힌트 `메시지를 입력하세요`, 가로 Fill 1.0, 변수 활성화
- `SizeBox_Send`: 88×48
- `Button_Send`: 변수 활성화
- `Text_Send`: `전송`

## 다음 작업

다음 세션에서는 `Button_Send.OnClicked`에 UE 5.8의 `Http Post Request` 노드를 연결한다.

1. 요청 시작 시 상태를 `Waiting`으로 바꾸고 버튼을 비활성화한다.
2. `http://127.0.0.1:8765/v1/conversations/respond`로 POST한다.
3. 첫 시험에서는 `Result Body` 원문을 `Text_Response`에 표시한다.
4. 왕복 성공 후 Blueprint Struct로 `dialogue`, `character`, `safety`, `feedback`을 파싱한다.
5. `character.animation`을 24개 Animation Sequence와 매핑한다.
6. 마지막에 모바일용 PC 사설 IP와 Windows 방화벽을 설정한다.

안전 판단과 ONN-C 상태 변경은 Unreal이나 표현 모델이 직접 결정하지 않는다. Unreal은 `onn-c.v1`에서 승인된 대사·상태·행동·안전 신호를 표현하는 클라이언트 역할을 유지한다.
