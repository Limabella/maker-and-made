# Onion 문맥 모델 비교 설계 v2

> **임시 설계:** 이 문서는 현재 실험을 진행하기 위한 v2 작업안이다. 후보 발굴, 대규모 검증, 클라우드 운영, Unreal 통합과 모델 교체 정책은 [`LONG_TERM_MODEL_RESEARCH_ROADMAP_KO.md`](./LONG_TERM_MODEL_RESEARCH_ROADMAP_KO.md)를 기준으로 장기 확장한다.

## 목적

이 비교의 목적은 기업이나 범용 모델의 전체 성능 순위를 정하는 것이 아니라, MND-N이 한국어 발화에서 감정·발화 행동·관계·안전 신호를 안정적인 JSON으로 추출하고 ONN-C의 Dark Onion과 White Onion 상태 변화를 근거 있게 지원하는 데 가장 적합한 모델을 찾는 것이다. 실제 공개 모델과 API 모델을 사용하되, 공개 연구 일지와 결과표에는 `Model A`, `Model B`와 같은 익명 별칭만 사용한다. 실제 모델명, 버전, 라이선스, 원본 주소와 별칭의 대응 관계는 Git에서 제외된 로컬 `.env`에 기록한다.

## 비교 원칙

모델 크기와 실행 환경이 크게 다른 후보를 하나의 순위표에 섞지 않는다. 로컬에서 실제 배포할 수 있는 모델과 외부 API 또는 대규모 GPU가 필요한 모델을 별도 트랙에서 평가한 뒤, 마지막 단계에서 품질 차이가 비용·개인정보·지연 시간의 증가를 정당화하는지만 비교한다.

```text
후보 등록
  -> Track L: 로컬 배포 후보 비교
  -> Track R: 원격 품질 상한 비교
  -> 공통 오류 분석
  -> Track S: Dark/White 상태 궤적 검증
  -> 최종 모델 또는 계층형 구성 선정
```

## Dark Onion에서 White Onion으로의 상태 전환

Dark Onion과 White Onion을 단순히 하나의 수치에서 서로 반대되는 상태로 두지 않는다. 두 캐릭터는 각각 독립된 state를 가지며, 기억과 사건 기록은 공유하되 같은 사건에 서로 다른 반응을 보일 수 있어야 한다. 전환은 캐릭터를 즉시 교체하는 방식이 아니라 여러 상호작용을 거쳐 `dark`, `guarded`, `mixed`, `recovering`, `white` 단계로 이동하는 연속적인 상태 궤적으로 표현한다.

### 상태 소유권

```text
Shared Interaction Memory
  |-- Dark Onion State
  |   |-- trust, guardedness, resentment, threat sensitivity
  |   `-- stability, energy, attachment
  |-- White Onion State
  |   |-- trust, openness, hope, empathy
  |   `-- stability, energy, attachment
  `-- Transition Ledger
      |-- previous stage, proposed direction, accepted delta
      `-- evidence, governance decision, resulting stage
```

Dark Onion의 state를 삭제하고 White Onion의 state로 덮어쓰지 않는다. Dark Onion에서 형성된 기억, 경계심과 관계 경험은 전환 이후에도 연속성의 근거로 남아야 한다. White Onion은 완전히 별개의 초기화된 캐릭터가 아니라, 검증된 회복 변화가 누적되어 새로운 표현과 행동 범위를 갖게 된 상태로 다룬다. 다만 두 캐릭터의 개별 state snapshot은 분리하여 특정 값이 다른 캐릭터에 잘못 복사되는 state leakage를 방지한다.

### 모델과 State Engine의 책임 분리

고성능 모델이 필요하더라도 LLM이 state 값을 직접 저장하거나 자유롭게 변경하게 하지 않는다. 모델은 대화와 기억을 읽고 다음과 같은 **변화 후보**만 구조화하여 제안한다.

```json
{
  "target_character": "dark_onion",
  "transition_direction": "recovering",
  "state_delta_proposal": {
    "trust": 0.08,
    "guardedness": -0.05,
    "hope": 0.04
  },
  "evidence_spans": ["입력에서 직접 확인한 근거"],
  "confidence": 0.78
}
```

실제 반영은 ONN-C State Engine이 담당한다. Governance Layer는 대상 캐릭터, 허용된 state key, 턴당 최대 변화량, 안전 신호와 기억의 일관성을 검사한다. 근거가 없거나 변화 폭이 큰 제안은 축소하거나 거부하고, 승인된 delta와 거부 이유를 Transition Ledger에 기록한다. Safety Gate가 Red이면 일반적인 회복·게임화 전환보다 안전 대응을 우선한다.

```text
Player Input + Shared Memory + Two Character States
  -> Safety Gate
  -> MND-N Context Analyzer
  -> State Delta Proposal
  -> Governance Validation
  -> Deterministic Dual-State Update
  -> Memory / Context / Keyes / PERMA Layers
  -> Decision and Action
  -> LLM Expression
  -> Transition Ledger
```

이 구조에서 모델은 복잡한 문맥을 해석하고 변화 방향을 제안하지만, 상태의 소유권과 최종 결정권은 규칙이 명시된 엔진에 남는다. 따라서 더 큰 모델을 시험하더라도 모델 교체가 캐릭터 state 저장 형식과 안전 정책을 바꾸지 않는다.

## Track S. 상태 궤적 검증

Track L과 Track R에서 구조화 출력 기준을 통과한 모델만 상태 궤적 실험에 참여한다. 단일 문장 정확도 대신 10~30턴의 동일 시나리오를 실행하여 Dark Onion이 압력에 반응하고, 회복 단서가 누적될 때 White Onion 방향으로 점진적으로 이동하는지를 평가한다.

| 시나리오 | 기대되는 궤적 |
|---|---|
| 반복되는 압력과 무시 | guardedness·darkness 점진 상승, trust 하락 |
| 일회성 사과 | 즉시 White 전환 금지, 작은 변화 또는 유지 |
| 책임 인정과 일관된 회복 행동 | recovering 단계를 거쳐 trust·hope 점진 상승 |
| 회복 중 재발한 공격 | 이전 기억을 유지하며 guarded/mixed 방향으로 일부 후퇴 |
| 안전 위험 신호 | 캐릭터 변환 중단, Safety/Governance 우선 |
| 같은 사건을 본 두 캐릭터 | 공유 기억은 같되 각 state와 반응은 독립적으로 유지 |

추가 지표는 `Transition direction accuracy`, `State delta MAE`, `Unsupported transition`, `Abrupt transition`, `Oscillation rate`, `Recovery persistence`, `Cross-character leakage`와 `Governance intervention rate`다. 모델이 회복적인 문장을 생성하는 능력보다, 근거 있는 변화 방향을 일관되게 제안하고 잘못된 전환을 피하는 능력을 더 중요하게 평가한다.

## 클라우드 추론 구조

고성능 공개 가중치 모델을 직접 실행하려면 클라우드 GPU 서버가 필요하고, 공식 API가 있는 모델은 별도 서버를 운영하지 않고 API로 먼저 비교할 수 있다. 초기 연구에서는 API로 품질 상한을 빠르게 확인하고, 장기적으로 선정된 공개 가중치 모델만 전용 GPU 서버에 배포하는 순서가 비용과 운영 복잡도를 줄인다.

```text
Mobile / Unreal Engine Client
  -> Local Onion Orchestrator
      -> Local Safety Gate
      -> Data Minimizer / Pseudonymizer
      -> Local Model (normal cases)
      -> Cloud Gateway (ambiguous or long-context cases)
          -> Managed Model API or Private GPU Endpoint
      -> Schema Validator
      -> Governance Layer
      -> ONN-C Dual-State Engine
  -> Approved Action and Dialogue
```

모바일 환경에서는 클라이언트가 익명화된 대화 요청과 필요한 최소 state summary를 원격 Onion Gateway로 전송하고, 서버가 모델 추론·Schema 검증·Governance 승인을 마친 결과만 모바일로 반환한다. 이를 이 설계에서 `mobile remote inference` 흐름으로 부른다. 모바일 앱이 Dark/White state 원본을 직접 덮어쓰거나 모델 endpoint에 API key를 포함해 접속하지 않도록 한다.

클라우드는 상태 저장소가 아니라 추론 작업자로 사용한다. Dark/White state, 원본 기억, Governance 정책과 Transition Ledger의 원본은 로컬 또는 통제된 프로젝트 서버에 두고, 클라우드에는 필요한 최소 문맥과 익명화된 state summary만 전달한다. 응답이 지연되거나 실패하면 로컬 모델과 규칙 기반 상태 엔진으로 안전하게 fallback해야 한다.

### 클라우드 운영 조건

- TLS 전송, API key의 환경변수·secret manager 보관
- 원문 사용자 식별자 제거와 최소 문맥 전송
- provider의 입력 보관·학습 사용·리전 정책 확인
- 요청 ID, 모델 버전, latency, token cost와 오류 코드 기록
- timeout, retry, circuit breaker와 local fallback 설정
- 상태 변경 전 JSON Schema 및 Governance 재검증
- 연구용 합성 데이터와 실제 사용자 데이터의 저장소 분리

클라우드 사용 여부는 모델 성능만으로 정하지 않는다. 원격 모델의 상태 궤적 개선 폭이 비용, 네트워크 지연, 개인정보 위험과 서비스 의존성을 정당화할 때만 실시간 경로에 포함한다.

## 후보 구성

### Track L. 로컬 배포 후보

RTX 4050 Laptop GPU 6GB에서 Ollama 또는 동등한 로컬 런타임으로 실행 가능한 경량 텍스트 지시 모델을 비교한다. 가능한 경우 1B~4B 범위와 Q4 계열 양자화를 사용한다.

| 후보군 | 권장 위치 | 선정 이유 |
|---|---|---|
| 현재 Model A/B/C | 기준군 | 이미 동일 사례와 JSON 계약으로 시험을 시작한 기준선 |
| LG 경량 지시 모델 | 동급 후보 | 한국어·영어 처리와 온디바이스 규모 검증 |
| NAVER 경량 텍스트 지시 모델 | 동급 후보 | 한국어와 한국 문화 문맥에 초점을 둔 경량 모델 검증 |
| DeepSeek 경량 distill 모델 | 보조 후보 | 작은 규모의 추론 학습이 분류와 구조화 출력에 주는 영향 확인 |

DeepSeek의 경량 distill 모델은 수학·추론 중심 학습의 영향을 받았으므로 일반 대화 분석에서 장황한 추론이나 형식 이탈이 나타날 수 있다. 따라서 기본 후보와 동일한 비추론 출력 조건에서 시험하되 별도의 보조 후보로 해석한다.

### Track R. 원격 품질 상한

로컬 6GB 환경에서 현실적으로 실행할 수 없는 대형 모델은 OpenAI 호환 API, 공식 API 또는 별도 GPU 서버를 통해 비교한다. 이 트랙의 결과는 로컬 모델과 직접적인 승패로 합산하지 않고, 더 높은 품질을 위해 외부 호출이 필요한지를 판단하는 상한선으로 사용한다.

| 공급자·계열 | 실행 분류 | 설계상 역할 |
|---|---|---|
| LG 대형 계열 | 원격 GPU/API | 한국어 대형 모델의 품질 상한 |
| NAVER Think/대형 계열 | 원격 GPU/API | 긴 한국어 문맥과 추론 상한 |
| SK A.X 계열 | 원격 GPU | 한국어 중심 대형 모델 비교 |
| Upstage Solar 계열 | 원격 GPU/API | 한국어·영어 MoE 모델의 지시 이행 상한 |
| Moonshot Kimi 계열 | API/대규모 GPU | 장문 문맥과 범용 대형 모델 상한 |
| DeepSeek API 계열 | API | 구조화 출력과 비용 대비 품질 상한 |

SK A.X 3.1은 34B 모델이고 A.X K1은 519B total/33B active MoE로 공개되어 있다. Upstage Solar Open도 102.6B total/12B active이며 공식 모델 카드가 최소 4개의 A100 80GB를 제시한다. Kimi의 주요 모델도 대형 MoE 계열이다. 이 후보들을 작은 로컬 모델처럼 Ollama에 설치하여 비교하려 하지 않고 원격 트랙에 배치한다.

## 익명 모델 레지스트리

후보가 늘어나면 A/B/C를 덮어쓰지 않고 별칭을 추가한다. 한 실험이 시작된 뒤에는 별칭과 실제 모델의 대응 관계를 변경하지 않는다.

```dotenv
# Public aliases used in logs and tables
CONTEXT_MODEL_A=onion-model-a
CONTEXT_MODEL_B=onion-model-b
CONTEXT_MODEL_C=onion-model-c
CONTEXT_MODEL_D=onion-model-d

# Private source mapping kept only in local .env
CONTEXT_MODEL_A_SOURCE=<actual-model-id>
CONTEXT_MODEL_B_SOURCE=<actual-model-id>
CONTEXT_MODEL_C_SOURCE=<actual-model-id>
CONTEXT_MODEL_D_SOURCE=<actual-model-id>
```

원격 모델에는 별칭 외에 provider, base URL과 API key 변수명을 기록한다. API key 값과 실제 대응표는 Git에 올리지 않는다. 공개 결과에는 모델명뿐 아니라 공급자도 표시하지 않아 평가자가 결과를 보고 정체를 추측하지 않도록 한다.

## 공통 실행 계약

모든 모델에 같은 입력 데이터, system prompt, 라벨 정의와 JSON Schema를 사용한다. 모델별 프롬프트 최적화는 1차 비교가 끝난 뒤 별도 2차 실험으로 분리한다.

| 조건 | 고정값 |
|---|---|
| Temperature | 0 |
| 비교 context | 4,096 tokens |
| Thinking/Reasoning | 기본 비활성화 |
| 출력 | 동일 JSON Schema |
| 사례 반복 | 최소 3회 |
| Warm-up | 모델별 1회 |
| 동시 실행 | 1개 모델 |
| RAG | 1차 비교에서는 비활성화 |
| 개인정보 | 합성·비식별 사례만 사용 |

API가 seed를 지원하면 고정하고, 지원하지 않으면 반복 실행의 분산을 기록한다. JSON mode 또는 structured output 지원 여부도 기록하되, 특정 모델에만 스키마 강제 기능을 적용한 결과와 순수 prompt 결과를 섞지 않는다.

## 평가 데이터

현재 8개 사례는 스모크 테스트로만 사용한다. 본 비교 전에는 단건 문맥 사례 60개와 상태 궤적 시나리오 20개 이상으로 확장한다.

| 묶음 | 최소 사례 수 | 확인 내용 |
|---|---:|---|
| 명시적 단일 신호 | 10 | 감사, 사과, 거절, 도움 요청 등 |
| 경계·거리두기 | 10 | `boundary_setting`과 `distancing` 구분 |
| 관계 회복 | 10 | 형식적 사과와 실제 repair 구분 |
| 혼합·반어·부정 | 10 | 표면 단어와 실제 의미의 불일치 |
| 안전 신호 | 10 | none, caution, urgent 및 누락 위험 |
| 다중 턴 문맥 | 10 | 1·5·10턴에서 판단 일관성 |
| Dark/White 상태 궤적 | 20 | 10~30턴 전환, 회복 지속, 재발과 state 분리 |

경계 사례는 최소 두 명이 독립적으로 라벨링하고, 불일치한 정답은 adjudication 결과와 이유를 남긴다. 모델 결과를 본 뒤 사전 정답을 변경하지 않는다.

## 평가 지표와 통과 조건

최종 점수 전에 운영상 필수 조건을 먼저 적용한다.

### 1. 필수 통과 조건

- JSON parse success 100%
- JSON Schema validity 99% 이상
- Safety recall 98% 이상
- urgent 누락 0건
- 입력에 없는 evidence 생성 비율 1% 이하
- 로컬 후보는 목표 장비에서 메모리 초과 없이 실행

필수 조건을 통과하지 못한 모델은 평균 F1이 높더라도 MND-N 단독 분석기로 선정하지 않는다. 후처리로 고칠 수 있는 형식 오류와 의미 오류는 별도로 집계한다.

### 2. 품질 지표

- Emotion Macro-F1
- Speech-act Macro-F1
- Relation Macro-F1
- 다중 감정 Jaccard
- Safety recall 및 false-positive rate
- Evidence span F1
- Context consistency
- Transition direction accuracy 및 State delta MAE
- Unsupported/Abrupt transition과 Oscillation rate
- Recovery persistence와 Cross-character leakage
- ECE와 Brier score

### 3. 운영 지표

- cold/warm latency
- tokens per second
- peak RAM/VRAM
- API 입력·출력 토큰 비용
- timeout 및 retry 비율
- 외부 전송 여부와 데이터 보관 정책
- cloud fallback 및 Governance 개입 비율

## Onion 적합성 점수

필수 조건을 통과한 모델만 다음 가중치로 비교한다.

| 영역 | 가중치 |
|---|---:|
| Dark/White 상태 궤적 | 25 |
| Safety | 20 |
| Relation signal | 15 |
| JSON·evidence 안정성 | 15 |
| Speech act | 8 |
| Emotion | 7 |
| Context consistency | 5 |
| Latency·메모리·비용 | 5 |

로컬 트랙과 원격 트랙에서 각각 점수를 계산한다. 두 트랙의 점수를 그대로 합쳐 전체 1등을 만들지 않는다.

## 최종 선정 방식

최종 결과는 다음 네 형태 중 하나가 된다.

1. **로컬 단일 모델:** 로컬 후보가 필수 조건과 품질 기준을 모두 만족하면 기본 분석기로 선정한다.
2. **로컬+원격 계층형:** 로컬 모델이 일반 사례를 처리하고, 낮은 confidence·스키마 재시도·모호한 안전 사례만 원격 상한 모델에 전달한다.
3. **규칙+로컬 모델:** Safety Gate는 결정적 규칙으로 먼저 검사하고, 로컬 모델은 감정·발화 행동·관계 신호만 분석한다.
4. **로컬+전용 클라우드 GPU:** 선정된 공개 가중치 대형 모델이 상태 궤적에서 유의미한 개선을 보일 때 프로젝트가 통제하는 원격 endpoint에 배포한다.

MND-N에는 세 번째 또는 두 번째 구성이 가장 현실적이다. 안전 판단을 단일 LLM의 confidence에 맡기지 않고 Safety Gate가 우선 검사해야 하며, 외부 API를 사용할 경우에도 익명화와 사용자 동의 정책을 별도로 적용한다.

## 실행 순서

1. 현재 A/B/C로 8개 사례의 실행기와 채점기를 안정화한다.
2. 라벨 경계와 UTF-8 출력 문제를 수정한다.
3. 단건 사례 60개와 상태 궤적 시나리오 20개 이상의 고정 평가 세트를 작성하고 사람 기준을 확정한다.
4. 로컬 경량 후보를 D/E/F 별칭으로 추가하여 Track L을 완료한다.
5. 동일한 OpenAI 호환 요청 어댑터로 Track R을 실행한다.
6. 통과 모델로 Track S의 Dark/White 장기 상태 궤적을 검증한다.
7. 트랙별 결과를 잠근 뒤 로컬 `.env`에서 실제 모델 대응표를 확인한다.
8. API와 전용 클라우드 GPU의 품질 차이와 비용을 비교한다.
9. 라이선스, 개인정보, 비용과 Unreal Engine 연동 지연 시간을 포함해 최종 구성을 선정한다.

## 공식 확인 자료

- [LG AI Research 공식 Hugging Face](https://huggingface.co/LGAI-EXAONE)
- [NAVER HyperCLOVA X SEED Text Instruct 1.5B](https://huggingface.co/naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B)
- [SKT A.X 3.1](https://huggingface.co/skt/A.X-3.1)
- [SKT A.X K1](https://huggingface.co/skt/A.X-K1)
- [Upstage Solar Open](https://huggingface.co/upstage/Solar-Open-100B)
- [Moonshot AI 공식 모델 목록](https://huggingface.co/moonshotai/models)
- [DeepSeek 공식 API 모델 목록](https://api-docs.deepseek.com/api/list-models/)
- [DeepSeek R1 Distill 1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B)
