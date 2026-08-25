# Maker-and-Made

Maker-and-Made(MaAM)는 캐릭터 AI, 상태 기반 에이전트, 안전한 지원 시스템을
프로젝트 단위로 연구하는 실험 저장소입니다.

현재 가장 활발한 프로젝트는 **OnionTest**입니다.

```text
OnionTest
└─ health-team
   ├─ ONN-C  Five Flavor Onion 캐릭터 엔진
   ├─ MND-N  비임상 정서 지원 및 안전 에이전트
   ├─ TRN-N  운동·신체 활동 지원 (합류 중)
   ├─ NTR-N  영양·생활 건강 지원 (예정)
   └─ CUR-N  역사적 연구 관점 (예정)
```

## 실행

저장소 루트에서 ONN-C CLI를 실행합니다.

```powershell
python src/projects/oniontest/teams/health-team/onn-c/play_cli.py
```

NVIDIA 호환 표현 모델을 사용하려면 다음과 같이 실행합니다.

```powershell
python src/projects/oniontest/teams/health-team/onn-c/play_cli.py --nvidia
```

상태·안전·정책 결정은 규칙 기반 계층이 담당하며, 외부 언어 모델은 표현만
보조합니다.

## 저장소 구조

```text
src/projects/
├─ oniontest/                # 상태형 캐릭터·건강 지원 에이전트
├─ manmijournel/             # 《만미록》 편집 에이전트 팀
└─ maam-kitchen-contest/     # 점심 메뉴봇 프로젝트와 로드맵

characters/                  # 프로젝트가 참조하는 캐릭터 원전
├─ <character-id>/
└─ archived/                 # 현재 실행·로드맵이 없는 캐릭터

docs/research/
├─ journal/                  # 날짜별 연구 일지
├─ ideas/                    # 아이디어 노트와 초기 제안
└─ experiments/              # 재현 가능한 실험·벤치마크

assets/images/               # 문서용 로컬 이미지; 원본 자산은 외부 저장소
artifacts/examples/          # 선별된 결과 예시
tools/prompts/               # 이미지·아카이브 제작 프롬프트
tests/                       # 저장소 공통 테스트
```

각 폴더의 책임은 다음과 같이 구분합니다.

- `src/projects/`: 실행 코드와 프로젝트별 역할 계약을 둡니다.
- `characters/`: 기존 MD 상단의 타입·분류를 보존하는 캐릭터 원전입니다.
- `docs/research/`: 연구 일지, 아이디어 노트, 실험을 분리해 관리합니다.
- `assets/images/`: 문서 호환을 위한 로컬 이미지입니다. 자산 원본은 [`Le-vela/character-assets`](https://github.com/Le-vela/character-assets)에서 관리합니다.
- `artifacts/examples/`: 문서에서 다시 볼 가치가 있는 결과만 둡니다.
- `tools/prompts/`: 런타임 에이전트 프롬프트가 아닌 제작 도구용 프롬프트만 둡니다.

일회성 실행 파일을 위한 `src/snippets/`는 사용하지 않습니다. 새로운 캐릭터
구현은 먼저 소속 프로젝트와 팀을 정한 뒤 해당 팀 폴더 안에 추가합니다.

## OnionTest 문서

| 영역 | 위치 |
|---|---|
| 프로젝트 개요 | [src/projects/oniontest](./src/projects/oniontest) |
| Health Team | [health-team](./src/projects/oniontest/teams/health-team) |
| ONN-C | [health-team/onn-c](./src/projects/oniontest/teams/health-team/onn-c) |
| MND-N | [health-team/mnd-n](./src/projects/oniontest/teams/health-team/mnd-n) |
| 연구 기록 | [docs/research](./docs/research) |
| 캐릭터 레지스트리 | [characters](./characters) |

## 안전 원칙

OnionTest는 임상 진단이나 치료 시스템이 아닙니다.

1. 사용자나 캐릭터를 병리적으로 진단하지 않습니다.
2. 안전 신호가 나타나면 게임화된 조언보다 안전 안내를 우선합니다.
3. 상태, 기억, 안전 및 정책 결정을 검사 가능한 코드로 유지합니다.
4. 언어 모델이 근거·안전 정책·캐릭터 상태를 임의로 결정하지 못하게 합니다.

## License

MIT License
