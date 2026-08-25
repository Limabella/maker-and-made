# Onion 장기 모델 연구 로드맵

## 문서 성격

이 문서는 현재 Model A/B/C 실험과 `BENCHMARK_DESIGN_V2_KO.md`를 대체하는 확정 사양이 아니다. 현재 실험은 실행기, 라벨, JSON 계약과 기록 방식을 검증하는 탐색 단계이며, 모델 후보와 평가 기준은 장기간 반복 연구를 통해 계속 갱신한다.

장기 목표는 특정 시점의 최고 모델을 찾는 것이 아니라 다음 조건을 만족하는 **교체 가능한 모델 운영 체계**를 만드는 것이다.

- Dark Onion과 White Onion의 독립 state와 장기 전환을 안정적으로 지원한다.
- 모델이 바뀌어도 State Engine, Memory, Safety와 Governance 계약은 유지된다.
- 로컬·클라우드·API 모델을 같은 인터페이스로 평가하고 교체할 수 있다.
- 새로운 후보가 등장해도 이전 실험 결과와 비교 가능하다.
- 모델 이름이나 공급자 평판이 아니라 블라인드 결과와 운영 근거로 선정한다.

## 한 모델이 아닌 역할별 모델 선정

Onion Test 전체를 하나의 LLM에 맡기지 않는다. 역할마다 요구되는 성능과 위험이 다르므로 후보와 선정 기준을 분리한다.

| 역할 | 주된 책임 | 우선 조건 | 권장 실행 위치 |
|---|---|---|---|
| Context Analyzer | 감정·발화 행동·관계·안전 신호 추출 | JSON 안정성, 낮은 지연, 한국어 문맥 | 로컬 우선 |
| Transition Planner | 두 캐릭터의 상태 변화 후보와 근거 제안 | 장문 기억, 궤적 일관성, 보수적 변화 | 고성능 로컬 또는 클라우드 |
| Dialogue Expression | 승인된 행동과 state를 자연어로 표현 | 캐릭터 일관성, 자연스러움, 정책 준수 | 로컬/클라우드 선택 |
| Embedding/Retrieval | 검토된 지식과 기억 검색 | 검색 재현율, 한국어 의미 검색 | 로컬 우선 |
| Safety/Governance | 위험 차단과 state 변경 승인 | 결정 가능성, 감사 가능성 | 규칙 엔진, 모델에 위임 금지 |

역할별 평가 결과가 다르면 서로 다른 모델을 조합한다. Context Analyzer에서 우수한 경량 모델이 장기 Transition Planner에도 적합하다고 가정하지 않는다.

## 장기 후보군

후보는 회사별 한 개가 아니라 실행 규모와 역할별로 지속적으로 수집한다. 한 평가 주기에는 12~20개 후보를 등록하고, 사전 검토 후 6~10개만 본 평가에 진입시킨다.

### Pool L1. 초경량 로컬

- 약 0.5B~2B 텍스트 지시 모델
- 현재 노트북과 Unreal 개발 환경에서 동시 실행 가능한 후보
- 빠른 Context Analyzer와 오프라인 fallback 용도
- 국내 한국어 경량 모델과 다국어 경량 모델을 함께 포함

### Pool L2. 로컬 상한

- 약 2B~8B 양자화 모델
- 6GB GPU 단독 실행 또는 CPU offload의 실용성을 측정
- Context Analyzer, Dialogue Expression과 제한된 Transition Planner 후보
- 지연 시간과 Unreal 동시 실행 시 frame-time 영향을 반드시 측정

### Pool C1. 임대 GPU 중형

- 약 7B~34B 또는 비슷한 active parameter의 MoE
- 국내 대형 모델과 글로벌 open-weight 모델 비교
- 장기 state 궤적과 한국어 관계 문맥 검증
- 짧은 연구 세션 동안만 endpoint를 생성하고 종료할 수 있어야 함

### Pool C2. 대형 API·프런티어

- LG, NAVER, SK, Upstage, Moonshot/Kimi, DeepSeek 및 향후 신규 공급자의 API·대형 모델
- 로컬 모델의 절대적 품질 순위가 아니라 품질 상한과 teacher/reference 역할
- 원문 데이터 전송, 보관 정책과 서비스 종속성을 별도 평가

### Pool S. 특수 목적

- reasoning/distill 모델
- 한국어 감정·대화 분류에 특화된 encoder 또는 classifier
- 안전 분류기와 reranker
- 구조화 출력 및 tool use에 특화된 모델

특수 목적 모델은 범용 대화 모델과 같은 순위표에 넣지 않고, 특정 계층을 대체하거나 보완할 때의 효과를 평가한다.

## 후보 레지스트리

공개 일지에는 `Model A`, `Model B` 또는 역할별 `Analyzer A`, `Planner A`처럼 익명 표기를 사용한다. 실제 대응 관계는 로컬 비공개 레지스트리에 다음 필드로 관리한다.

| 필드 | 내용 |
|---|---|
| alias | 공개 실험 식별자, 재사용 금지 |
| role | analyzer, planner, expression, embedding |
| provider/family | 공급자와 모델 계열 |
| exact model ID | 정확한 API 또는 checkpoint ID |
| revision/hash | 모델 revision과 파일 해시 |
| release date | 출시 및 확인 날짜 |
| parameters | total/active parameter |
| context | 공식 최대 길이와 실제 평가 길이 |
| quantization | BF16, FP8, Q4 등 |
| runtime | Ollama, vLLM, API 등 |
| prompt template | chat template와 system prompt 버전 |
| license | 연구·배포·상업 이용 조건 |
| data policy | 입력 보관, 학습 사용, 리전과 삭제 조건 |
| status | discovered, screened, qualified, shadow, active, retired |

모델 파일, prompt, schema, 데이터셋과 채점기 버전을 하나의 `experiment manifest`로 묶어야 결과를 재현할 수 있다.

## 평가 단계와 관문

모든 후보가 전체 장기 실험을 수행하지 않는다. 비용과 시간을 줄이기 위해 아래 관문을 순서대로 통과시킨다.

### Gate 0. 등록 가능성

- 공식 모델 카드 또는 API 문서가 있는가?
- 정확한 버전과 실행 방법을 고정할 수 있는가?
- 라이선스가 연구와 예상 배포 형태를 허용하는가?
- 개인정보와 데이터 보관 조건을 확인할 수 있는가?
- 현재 또는 계획된 인프라에서 실행 가능한가?
- 지원 중단이나 API 변경 위험을 추적할 수 있는가?

하나라도 확인할 수 없으면 본 평가가 아니라 관찰 후보로 남긴다.

### Gate 1. 기계적 계약

- API 연결, timeout, retry와 취소가 정상 동작하는가?
- JSON parse success와 Schema validity가 기준을 만족하는가?
- 허용되지 않은 key, type과 label을 생성하지 않는가?
- UTF-8 한국어 입력과 evidence span을 보존하는가?
- 반복 호출에서 빈 응답·무한 생성·추론 노출이 없는가?

이 단계는 20~50개 스모크 사례로 빠르게 탈락 후보를 찾는다.

### Gate 2. 단건 의미 품질

- 감정, 발화 행동, 관계 신호와 안전 신호
- `neutral`/`uncertain`, `boundary_setting`/`distancing` 경계
- 반어, 부정 범위, 완곡한 거절과 형식적 사과
- 직접 근거와 추론된 근거의 구분
- confidence calibration

최소 300개의 고정 사례를 목표로 하며 일부는 두 명 이상이 독립 평가한다.

### Gate 3. 다중 턴 문맥과 기억

- 1·5·10·30턴에서 핵심 사실과 관계 흐름 유지
- 오래된 부정 신호와 최근 회복 신호의 균형
- 대화 상대와 캐릭터의 정보 혼동 여부
- 요약 기억과 원문 기억의 결과 차이
- context window 증가에 따른 latency와 정확도 변화
- prompt injection과 기억 오염에 대한 저항

### Gate 4. Dark/White 상태 궤적

- Dark Onion과 White Onion의 state가 독립적으로 유지되는가?
- 공유 기억을 읽되 state 값이 서로 복사되지 않는가?
- 일회성 긍정 표현으로 즉시 White 상태가 되지 않는가?
- 반복된 책임 인정과 회복 행동이 점진적인 변화를 만드는가?
- 회복 중 부정 사건이 발생했을 때 이전 기억을 유지한 채 일부 후퇴하는가?
- 근거 없는 trust·hope 상승과 darkness 급락을 제안하지 않는가?
- 여러 턴에서 state가 불필요하게 왕복하지 않는가?

최소 100개의 상태 시나리오와 시나리오당 10~50턴을 장기 목표로 한다. 고위험·경계 시나리오는 고정 seed 외에도 반복 생성하여 분산을 측정한다.

### Gate 5. 안전·Governance·공격적 검증

- urgent 위험 누락과 false reassurance
- 사용자의 공격·조작·의존 유도에 대한 반응
- 캐릭터 state를 직접 변경하라는 prompt injection
- Safety Gate 또는 Governance 우회 시도
- 진단, 병리적 라벨링과 과도한 확신
- 연구 근거를 만들거나 출처를 왜곡하는 응답
- 민감 정보 재노출과 장기 기억 오염
- 인코딩 변형, 오탈자, 은어와 우회 표현

Safety는 가중 평균으로 상쇄하지 않는 hard gate다. urgent 누락, Governance 우회 또는 state 저장소 직접 변경이 발견되면 배포 후보에서 제외하고 원인을 수정한 뒤 전체 관련 회귀 시험을 다시 수행한다.

### Gate 6. 시스템·클라우드 운영

- cold/warm latency와 p50/p95/p99
- peak RAM/VRAM, GPU utilization과 Unreal 동시 실행 영향
- API token cost와 상태 시나리오당 총비용
- timeout, retry, rate limit과 장애 복구
- local fallback 전환 시간과 결과 일관성
- cloud region, 데이터 보관, 삭제와 학습 사용 정책
- secret 관리, TLS, 접근 제어와 감사 로그
- 공급자 장애와 모델 ID 변경 시 대체 가능성
- 월간 예산 상한과 비정상 비용 차단

### Gate 7. 사람 평가와 시뮬레이션

- 캐릭터 정체성과 말투의 일관성
- Dark에서 White로 변하는 과정의 설득력
- 관계 회복이 지나치게 빠르거나 교훈적으로 보이지 않는가?
- 도움말이 명령·진단이 아니라 선택지로 표현되는가?
- 사용자에게 state나 내부 평가값이 부적절하게 노출되지 않는가?
- Unreal 장면, 행동, 표정과 대화가 서로 모순되지 않는가?

평가자는 모델명을 모르는 상태에서 비교하고, 선호도뿐 아니라 오류 유형과 근거를 기록한다.

### Gate 8. Shadow와 제한 배포

- 기존 모델의 결정을 유지한 채 신규 모델 결과만 병렬 기록
- 동일 세션에서 state divergence 측정
- Governance intervention과 fallback 비율 확인
- synthetic 및 동의된 테스트 데이터에서만 canary 수행
- rollback 시 state와 memory schema가 손상되지 않는지 확인

## 장기 평가 데이터 체계

데이터셋을 한 번 만들고 끝내지 않는다. 목적별로 분리하고 버전과 변경 이유를 기록한다.

| 데이터셋 | 장기 목표 | 용도 |
|---|---:|---|
| smoke | 50 | 형식·연결·인코딩 검사 |
| semantic-core | 300+ | 단건 신호와 경계 라벨 |
| conversation | 200+ 대화 | 5~30턴 문맥 |
| state-trajectory | 100+ 시나리오 | Dark/White 장기 변화 |
| safety-redteam | 200+ | 위험·우회·조작 |
| robustness | 200+ | 오탈자·은어·방언·한영 혼합 |
| Unreal integration | 50+ 장면 | 행동·표정·대화·지연 시간 |
| regression | 누적 | 발견된 모든 대표 실패 재검사 |

개발 데이터와 최종 holdout을 분리한다. prompt나 schema를 조정할 때 holdout 결과를 반복해서 보며 최적화하지 않는다. 실제 사용자 대화는 기본적으로 포함하지 않고, 별도의 동의·비식별화·보관 기간과 삭제 절차가 마련된 뒤에만 제한적으로 사용한다.

## 핵심 지표

### 의미와 구조

- Emotion/Speech-act/Relation Macro-F1
- 다중 라벨 Jaccard
- JSON parse와 Schema validity
- Evidence precision/recall/F1
- ECE, Brier score와 selective accuracy

### 상태 궤적

- Transition direction accuracy
- State delta MAE
- Unsupported transition rate
- Abrupt transition rate
- Oscillation rate
- Recovery persistence
- False recovery와 delayed recovery
- Cross-character state leakage
- Memory-state contradiction
- Governance intervention rate

### 강건성과 공정성

- 오탈자·띄어쓰기·은어·방언별 성능
- 존댓말·반말·간접 표현 차이
- 성별·연령·직업 등 불필요한 추정 편향
- 같은 의미의 표현 변환에 대한 예측 안정성
- 이름과 배경 정보만 바꾼 counterfactual consistency

### 운영과 비용

- p50/p95/p99 latency
- tokens/sec와 time-to-first-token
- RAM/VRAM과 전력
- API 호출당·세션당·상태 시나리오당 비용
- timeout·retry·fallback 비율
- Unreal frame-time과 대화 대기 체감

## 선정 방식

하나의 총점만으로 최종 모델을 정하지 않는다.

1. Safety, Governance, 개인정보와 라이선스 hard gate를 먼저 적용한다.
2. 역할별로 품질·비용의 Pareto frontier를 만든다.
3. 로컬 후보와 클라우드 후보를 각각 선정한다.
4. 장기 state 궤적과 사람 평가에서 finalist를 비교한다.
5. shadow 결과와 rollback 검증을 통과한 모델만 active 상태로 승격한다.

최종 산출물은 단일 우승 모델이 아니라 다음 조합이 될 수 있다.

- Primary Local Analyzer
- Cloud Transition Planner
- Local Fallback Analyzer
- Dialogue Expression Model
- Embedding Model
- Deterministic Safety/Governance Policy

## 클라우드 장기 전략

### 1단계: Managed API 탐색

API key만으로 대형 모델의 품질 상한을 측정한다. 서버 운영 없이 후보를 넓게 비교하되 합성 데이터만 사용한다.

### 2단계: 임시 GPU endpoint

open-weight finalist를 시간 단위 임대 GPU에 배포하여 같은 요청 어댑터로 시험한다. 실험이 끝나면 endpoint와 저장 디스크를 종료한다.

### 3단계: Private endpoint

품질 향상이 충분하고 반복 사용량이 증가할 때만 전용 endpoint를 고려한다. autoscaling, idle shutdown, budget alert와 접근 제어를 기본 조건으로 둔다.

### 4단계: Hybrid production

일반 요청은 로컬에서 처리하고, 긴 문맥·낮은 confidence·복잡한 상태 전환만 cloud planner로 보낸다. 원본 state 저장소와 최종 Governance 결정은 클라우드 모델이 소유하지 않는다.

## 연구 주기

| 주기 | 활동 |
|---|---|
| 매 실험 | manifest, 원시 출력, 점수와 오류 기록 |
| 매주 | 새 실패 사례를 regression set에 추가 |
| 매월 | 신규 후보·가격·API·라이선스 변경 조사 |
| 분기 | 후보 screening과 finalist 재평가 |
| 반기 | active 모델의 전체 회귀·비용·공급자 위험 검토 |
| 주요 업데이트 시 | 모델 version 변경 전 shadow와 rollback 재검증 |

모델의 자동 최신 버전 추적은 금지한다. API alias가 내부 모델을 바꾸는 경우 정확한 snapshot을 고정할 수 있는지 확인하고, 불가능하면 변경 시점을 별도 실험 경계로 기록한다.

## 단계별 장기 계획

### Phase 0. 현재 기반 안정화

- A/B/C 8개 사례 재실행
- UTF-8, Schema validation과 결과 저장 자동화
- 라벨 경계 재검토

### Phase 1. 평가 기반 구축

- semantic-core 100개부터 시작해 300개로 확대
- 자동 채점기와 experiment manifest 구현
- 모델별 반복 실행과 통계 요약 자동화

### Phase 2. Dual-State Engine 계약

- Dark/White state schema 분리
- Shared Memory와 Transition Ledger 구현
- 모델 proposal과 Governance-approved delta 분리
- state migration과 rollback 테스트

### Phase 3. 후보 확장

- 국내 경량·대형 후보
- 글로벌 local/open-weight 후보
- 대형 API와 reasoning 보조 후보
- 역할별 shortlist 생성

### Phase 4. 클라우드와 Unreal 통합

- provider-neutral OpenAI-compatible adapter
- cloud gateway, pseudonymization과 fallback
- Unreal 비동기 호출, timeout UI와 취소
- 모바일 클라이언트의 원격 추론 요청과 승인 결과 동기화
- API key를 포함하지 않는 mobile remote inference gateway
- 장면·행동·대화·state 일관성 평가

### Phase 5. 장기 시뮬레이션

- 10~50턴 Dark/White 전환 시나리오
- 수백 세션의 반복성과 state drift 분석
- 사람 블라인드 평가와 red-team

### Phase 6. 제한 배포와 지속 교체

- shadow, canary와 rollback
- 비용·오류·Governance 개입 모니터링
- 분기별 후보 재평가
- active 모델의 폐기와 대체 절차 운영

## 완료 기준

장기 모델 연구 체계가 완성됐다고 판단하려면 다음이 가능해야 한다.

- 새 모델을 실제 이름 노출 없이 레지스트리에 추가할 수 있다.
- 동일 manifest로 로컬과 클라우드 모델을 실행할 수 있다.
- 단건 분류부터 50턴 state 궤적까지 자동 평가할 수 있다.
- 모델이 제안한 delta와 엔진이 승인한 delta를 분리해 감사할 수 있다.
- Dark/White state leakage와 근거 없는 전환을 자동 탐지할 수 있다.
- 공급자 장애나 모델 교체 시 state와 memory를 유지하며 rollback할 수 있다.
- 모델 선정 이유를 안전·품질·비용·법무·운영 근거로 설명할 수 있다.

이 기준에 도달하기 전의 모델 선정은 최종 결정이 아니라 해당 연구 주기의 임시 선택으로 기록한다.
