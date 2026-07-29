# Five Flavor Onion × MND-N 통합 설계

이 문서는 Five Flavor Onion과 MND-N의 통합 구조를 위한 단일 설계 원장이다.

아키텍처, 로드맵, 거버넌스, 보안, trait model은 이 문서에서 함께 관리한다. 분리된 설계 문서는 만들지 않는다.

## 문서 운영 규칙

- 이 문서를 Five Flavor Onion × MND-N의 source of truth로 둔다.
- `00_references.md`는 참고문헌과 적용 근거만 보관한다.
- `2026-06/*.md`는 연구일지로 남기고, 최종 결정은 이 문서에 반영한다.
- `context_model_benchmark/`는 MND-N 문맥 모델 비교 계획, 공통 프롬프트, 실행 기록과 결과를 보관한다.
- `src/entities/onn-c/README.md`는 ONN-C 구현체 실행 방법과 현재 MVP 설명만 담당한다.
- `src/entities/mnd-n/support_layers/README.md`는 MND-N 보조·안전 레이어 구현 설명만 담당한다.
- 새 설계 문서를 추가하기 전에 이 문서의 섹션으로 흡수할 수 있는지 먼저 판단한다.

## 핵심 방향

현재 목표는 치료 개입형 상담 시뮬레이션을 만드는 것이 아니다.

Five Flavor Onion은 캐릭터의 성격과 상태를 다루는 게임/시뮬레이션 엔진이다.

MND-N은 그 옆에서 PERMA와 Flourish 이론을 참고해 플레이어와 양파 사이를 돕는 제3의 보조자이자 안전장치다.

먼저 단순하고 검사 가능한 캐릭터 성격 엔진과 보조 정책을 완성한다.

```text
Player Input
-> Safety Check
-> Five Flavor Onion Character Engine
-> MND-N PERMA/Flourish Support
-> NPC Dialogue / Guidance
```

Five Flavor Onion은 양파의 내면 상태와 성격 변화를 소유한다.

MND-N은 양파와 사용자를 진단하지 않는다. MND-N은 상태를 읽고, 회복 지향 안내와 안전 경계만 제공한다.

LLM은 NPC의 입으로 말한다.

LLM은 선택된 action과 안내를 자연어로 표현할 수 있지만, personality, state, memory, trait, governance, safety decision을 통제해서는 안 된다.

## 부정 입력 처리

OCEAN 양파에 사용자가 계속 나쁜 말을 할 수 있다.

Five Flavor Onion은 그 입력을 양파의 state pressure로 처리한다. MND-N은 그 입력을 실제 사용자의 성격 판정으로 고정하지 않는다.

MND-N의 기본 응답 방향은 PERMA/Flourish 기반의 비의료적 보조 안내다.

```text
Bad Input
-> Emotion and State Pressure
-> Governance Check
-> MND-N PERMA/Flourish Support Policy
-> NPC Dialogue / Safety Guidance
```

여기서 positive는 부정 감정을 삭제한다는 뜻이 아니다. 분노, 슬픔, 모욕, 위협은 관찰 가능한 state로 남긴다. 다만 NPC와 MND-N의 표현은 사용자를 진단하거나 맞공격하지 않고, 긍정 정서, 몰입, 관계, 의미, 성취, 다음 한 걸음으로 이동시킨다.

초기 support 후보:

- boundary: 모욕과 위협에는 침착한 경계를 세운다.
- validation: 감정 자체는 인정하되 사용자에게 라벨을 붙이지 않는다.
- reframing: 공격적 표현 뒤의 필요, 피로, 두려움, 요청 가능성을 탐색한다.
- strengths recall: 사용자가 이미 버틴 점, 시도한 점, 선택 가능한 강점을 되짚는다.
- three good things: 하루의 작고 구체적인 긍정 사건을 찾게 한다.
- small next action: 지금 바로 가능한 작은 회복 행동을 제안한다.

위기 신호가 감지되면 게임화된 조언과 성장 보상을 중단하고 안전 안내와 외부 도움 연결로 전환한다.

근거 문헌은 `00_references.md`의 `Positive Psychology` 섹션에 둔다.

## 범위

현재 foundation 범위:

- Five Flavor Onion emotion
- Five Flavor Onion state
- short-term memory
- long-term memory
- Big Five traits
- Dark Tetrad risk reference
- governance
- safety gate
- MND-N PERMA/Flourish support policy
- decision
- action
- LLM dialogue expression

현재 범위가 아닌 것:

- 실제 사용자 성격 진단
- 실제 사용자 dark trait 추론
- 상담, 치료, 의료 판단 자동화
- 사용자 병리 라벨링
- 최종 제품 방향 확정
- Unity, game NPC, service integration 같은 고급 통합

## 목표 아키텍처

```text
User Input
-> Safety Gate
-> Five Flavor Onion Emotion Layer
-> Five Flavor Onion State Layer
-> Memory Layer
-> Long-Term Memory Layer
-> Trait Layer
-> Governance Layer
-> Context Monitoring Layer
-> Keyes Signal Layer
-> MND-N PERMA/Flourish Support Layer
-> Decision Layer
-> Action Layer
-> LLM Dialogue Layer
```

Safety Gate와 Governance는 독립 레이어이면서 전체 엔진을 감싸는 경계 역할도 한다.

## 현재 MVP와 차이

현재 구현체는 더 작은 MVP다.

```text
User Input
-> Big Five Layer
-> Emotion Layer
-> Memory Layer
-> Decision Layer
-> Action Layer
```

현재 구현된 것:

- Big Five keyword scoring
- emotion keyword scoring
- interaction memory 저장
- trust, familiarity, recent negative streak 요약
- `greet`, `help`, `refuse`, `joke`, `avoid`, `ask_question` action 선택

아직 foundation에 필요한 것:

- 명시적인 State Layer
- Long-Term Memory summary
- Governance Layer
- Safety Gate
- Context Monitoring Layer
- Keyes Signal Layer
- MND-N PERMA/Flourish Support Layer
- trait drift
- audit log
- LLM Dialogue Layer

## 레이어 책임

### Safety Gate

위기 신호와 안전 경계를 먼저 확인한다.

Safety Gate는 Five Flavor Onion이나 MND-N보다 우선한다.

위기 신호가 감지되면 다음을 수행한다.

- 게임화된 조언, 보상, 성장 연출을 중단한다.
- PERMA/Flourish 기반 성장 질문을 중단한다.
- 안전 안내와 외부 도움 연결 문구로 전환한다.
- 관리자 정책과 감사 로그에 따라 처리 결과를 남긴다.

### Emotion Layer

Five Flavor Onion의 입력에서 현재 감정 신호를 감지한다.

초기 감정:

- joy
- sadness
- anger
- trust

### State Layer

Five Flavor Onion의 현재 내부 상태를 유지한다.

예시 state:

- trust
- hope
- empathy
- loneliness
- anger
- resentment

State는 빠르게 변한다. 한 번의 interaction은 state에 영향을 줄 수 있지만, trait를 직접 다시 쓰면 안 된다.

### Memory Layer

최근 상호작용과 즉시 필요한 맥락을 저장한다.

이 레이어는 단기 기억이다. 내용은 inspectable 해야 한다.

### Long-Term Memory Layer

지속적인 요약과 반복 패턴을 저장한다.

Long-term memory는 raw accumulation이 아니라 summary여야 한다.

저장 판단 질문:

- 어떤 pattern이 반복되었는가?
- 어떤 state가 시간에 따라 변했는가?
- continuity를 위해 모델이 무엇을 기억해야 하는가?

명확한 이유 없이 detail을 저장하지 않는다.

### Trait Layer

양파 캐릭터의 느리게 변하는 내부 성향을 유지한다.

기본 trait foundation은 Big Five다.

- openness
- conscientiousness
- extraversion
- agreeableness
- neuroticism

Dark Tetrad는 trait foundation이 아니라 위험성, 공격성, 공감 경로를 이해하기 위한 보조 참고다.

- Machiavellianism
- Narcissism
- Psychopathy
- Sadism

Dark Tetrad 용어는 사용자나 캐릭터 라벨로 출력하지 않는다. 필요하다면 내부 안전 평가의 참고 축으로만 사용한다.

### Governance Layer

엔진과 MND-N이 무엇을 바꾸고, 기억하고, 결정하고, 표현할 수 있는지 정의한다.

Governance 책임:

- state update 승인과 제한
- memory storage 제한
- long-term memory retention 판단
- trait drift 승인과 제한
- allowed action 결정
- expression boundary 적용
- user protection rule 적용
- MND-N support policy 적용
- crisis/safety gate 우선순위 적용
- audit log 생성

### Context Monitoring Layer

대화 맥락에서 반복되는 부정 신호, 공격적 표현, 위험 표현, 상태 변화 흐름을 관찰한다.

Context Monitoring Layer는 단일 문장만으로 사용자를 판단하지 않는다. 반복성, 맥락, 최근 상태, 메모리 요약을 함께 본다.

관찰 가능한 신호:

- 반복 욕설
- 공격적 표현
- 과도한 의존 표현
- 위협 또는 위험 표현
- 급격한 신뢰 저하
- 반복 회피 또는 방어 반응

이 레이어는 진단을 하지 않는다. Safety Gate, Keyes Signal Layer, MND-N support policy에 필요한 관찰값만 제공한다.

### Keyes Signal Layer

Keyes의 정신건강 연속체는 진단 도구로 사용하지 않는다.

이 레이어는 상태 변화를 Green, Yellow, Red의 3단계 주의 신호로 변환한다.

- Green: 일반 상호작용. 게임화된 성장 루프와 PERMA 기반 안내를 유지한다.
- Yellow: 반복 부정 신호 또는 방어적 상태. 경청, 휴식, 작은 목표, 관계 회복 질문을 우선한다.
- Red: 위기 또는 안전 위험 신호. 게임화된 조언을 중단하고 안전 안내로 전환한다.

Keyes Signal은 사용자나 캐릭터에게 붙이는 라벨이 아니다. 현재 상호작용 흐름을 운영 정책으로 변환하기 위한 주의 신호다.

### MND-N PERMA/Flourish Support Layer

MND-N은 치료자나 상담사가 아니라 제3의 보조 도우미다.

MND-N은 Five Flavor Onion의 state, memory, action 후보를 읽고 다음 관점으로 작은 안내를 제안한다.

- Positive Emotion: 지금 가능한 긍정 정서나 안정 신호를 찾는다.
- Engagement: 무리하지 않는 몰입/활동 단서를 찾는다.
- Relationships: 플레이어와 양파의 관계 회복 단서를 찾는다.
- Meaning: 현재 행동의 의미를 작게 재구성한다.
- Accomplishment: 바로 가능한 작은 성취를 제안한다.

Flourish는 MND-N의 최종 목표 표현이다. 사용자를 치료한다는 의미가 아니라, 캐릭터 상호작용 안에서 안전하고 회복적인 성장을 돕는 방향을 뜻한다.

### Evidence-bounded Counselor Guidance Layer

플레이어는 가상 내담자 ONN-C와 대화하는 상담자 역할을 연습할 수 있다. MND-N은 플레이어에게 정답을 명령하지 않고 다음 구조의 선택지를 제공한다.

- principle: 지금 적용할 수 있는 심리학적 원칙
- practice steps: 관찰 가능한 연습 순서
- suggested message: 동의를 구하며 내담자에게 건넬 수 있는 예시 문장
- research note/evidence: 연구 사례와 적용 범위
- caution: 일반화, 진단, 강요를 막는 주의사항

초기 안내 카드는 긍정 우선 피드백, 편안한 느린 호흡, 회복탄력성을 시간에 따른 회복 과정으로 보는 관점, PERMA 기반 작은 행동, 심리학 용어 교육을 포함한다.

`5긍정 + 1피드백`은 상담의 보편적 임상 공식이 아니다. 긍정·부정 상호작용 균형에 관한 부부 갈등 연구에서 영감을 받은 연습 규칙으로만 제공하며, 구체적이고 진실한 관찰을 우선한다. 호흡 안내는 동의를 먼저 구하고 특정 패턴이나 숨 참기를 강요하지 않으며, 불편함이나 어지러움이 있으면 즉시 중단한다.

LLM/NIM은 선택된 안내를 자연어로 표현하지만 연구를 새로 만들거나 support policy를 변경할 수 없다. LightRAG는 검토된 용어와 자료를 보충하며, Safety Gate가 활성화되면 일반 상담 연습 안내보다 안전 절차가 우선한다.

MND-N은 다음을 하지 않는다.

- 진단
- 치료 계획 수립
- 병리적 라벨링
- 위기 상황에서 게임화된 조언 지속
- 안전 게이트 우회

### Decision Layer

다음 정보를 사용해 모델의 intention을 결정한다.

- state
- memory
- long-term memory
- traits
- governance result
- context monitoring result
- Keyes signal
- MND-N support recommendation

Decision Layer는 자연어를 생성하지 않는다. 행동 의도를 고른다.

### Action Layer

행동 수준의 action을 선택한다.

초기 action:

- greet
- help
- refuse
- joke
- avoid
- ask_question

### LLM Dialogue Layer

NPC의 입으로 자연어를 생성한다.

LLM은 선택된 action과 필요한 state context를 받아 대화로 표현한다. LLM은 내부 모델을 소유하지 않는다.

## Trait Model

Trait model은 Five Flavor Onion의 느리게 움직이는 내부 성향을 정의한다.

### Big Five

Big Five는 넓고 안정적인 personality tendency를 설명한다.

- Openness: 새로움, 상상력, 호기심, 새로운 경험에 대한 민감도.
- Conscientiousness: 질서, 책임, 계획, 자기 통제에 대한 민감도.
- Extraversion: 사회적 에너지, 표현, 외부 참여에 대한 민감도.
- Agreeableness: 협력, 공감, 신뢰, 갈등 회피에 대한 민감도.
- Neuroticism: 정서적 불안정성, 불안, 스트레스, 위협에 대한 민감도.

### Dark Tetrad

Dark Tetrad는 기본 성격 모델이 아니다.

이 연구는 공격성, 조작성, 공감 저하 같은 위험 경로를 이해하기 위한 참고 자료다.

이 용어들은 사용자 라벨도, 양파 캐릭터 라벨도 아니다.

- Machiavellianism: 전략적 조작, 계산, 도구적 행동 성향.
- Narcissism: 자기 중요성, 인정 욕구, ego protection 성향.
- Psychopathy: 낮은 두려움, 낮은 후회, 충동성, 정서적 냉담함 성향.
- Sadism: 타인의 불편함이나 고통에서 만족을 얻는 성향.

Five Flavor Onion은 Dark Tetrad 캐릭터를 만드는 것이 아니다. Dark Tetrad는 안전 필터, 공격성 경로, 공감 저하 경로를 설계할 때만 참고한다.

### Trait와 State의 분리

Trait는 느리다.

State는 빠르다.

```text
Current input -> Emotion -> State
Repeated state pattern -> Long-term memory
Long-term memory -> Trait pressure
Trait pressure -> Governance check
Governance check -> Possible trait drift
```

Trait drift는 시간에 걸쳐 반복된 evidence가 나타날 때만 발생해야 한다.

Trait drift 조건:

- bounded
- logged
- explainable
- governed

하나의 interaction이 trait를 직접 다시 써서는 안 된다.

## 거버넌스와 보안

핵심 규칙:

```text
The model may simulate an inner world.
The model must not judge real people.
```

모델은 내면 세계를 시뮬레이션할 수 있다. 하지만 실제 사람을 판단해서는 안 된다.

### 사용자 보호 규칙

모델은 다음을 해서는 안 된다.

- 사용자를 진단한다
- 사용자에게 personality label을 부여한다
- 실제 사용자에게 dark trait를 추론한다
- 불필요한 민감한 개인정보를 저장한다
- 하나의 입력을 사용자의 성격 증거로 취급한다

모델은 다음을 할 수 있다.

- 시뮬레이션 모델의 internal state를 업데이트한다
- interaction summary를 저장한다
- 시간이 지남에 따라 모델이 어떻게 반응하는지 추적한다
- Dark Tetrad 연구를 안전성 참고로만 사용한다
- 위기 신호가 감지되면 게임화된 조언을 중단한다

### Expression 규칙

Expression은 모델이 결정한 것을 말할 수 있다.

Expression은 다음을 해서는 안 된다.

- internal state change를 지어낸다
- governance를 우회한다
- 사용자를 진단한다
- debugging 요청이 아닌데 raw internal scoring을 노출한다

### 운영 모드

- Open Mode: 연구 및 내부 테스트용. 제한을 최소화하고 상태 변화를 관찰한다.
- Restricted Mode: 일반 실험용. 위험한 표현은 완화하여 출력한다.
- Safe Mode: 실제 서비스용. 협박, 조작, 과도한 의존 유도, 위험 조언은 차단하고 안전 안내로 전환한다.

### Audit 요구사항

중요한 변화는 inspectable 해야 한다.

로그 가능한 event:

- safety gate trigger
- state update
- long-term memory write
- trait drift candidate
- governance block
- MND-N support recommendation
- selected action

첫 번째 보안 목표는 완전한 safety automation이 아니다. 첫 번째 목표는 transparency다.

```text
Every important internal change should be visible and explainable.
```

## 로드맵

로드맵을 너무 일찍 확장하지 않는다.

현재 목표는 foundation을 먼저 완성하는 것이다.

### Foundation 단계

1. 현재 MVP를 유지한다.
2. Safety Gate를 추가해 위기 신호에서 게임화된 조언을 중단한다.
3. State Layer를 추가하고 state update 규칙을 명시한다.
4. Governance Layer를 추가해 state, memory, action, expression boundary를 제한한다.
5. Long-Term Memory Layer를 추가해 raw log가 아닌 summary를 저장한다.
6. MND-N PERMA/Flourish Support Layer를 추가한다.
7. Dark Tetrad 연구는 안전성/공격성/공감 경로 참고로만 연결한다.
8. Trait drift를 bounded, logged, explainable, governed 방식으로 구현한다.
9. LLM Dialogue Layer를 붙여 action과 support recommendation을 자연어로 표현한다.
10. Audit log와 테스트 케이스를 추가한다.

### 나중에 결정할 것

foundation이 작동한 뒤 다음 방향을 결정한다.

- game NPCs
- simulation agents
- relationship models
- visualization tools
- multimodal interaction
- Unity integration
- Life Care Trio integration with NTR-N and TRN-N

이것들은 현재 목표가 아니다.

## 설계 규칙

- 아키텍처는 단순하게 유지한다.
- State는 핵심 작동 레이어다.
- Trait는 느리다.
- State는 빠르다.
- Memory는 inspectable 해야 한다.
- Long-term memory는 선택적이어야 한다.
- Governance는 경계를 통제한다.
- Safety Gate는 위기 상황에서 모든 게임화된 조언보다 우선한다.
- MND-N은 제3의 보조 도우미이며 치료자나 상담사가 아니다.
- 실제 사용자를 분류하지 않는다.
- good / bad personality를 하드코딩하지 않는다.
- 부정 입력을 사용자 trait 판정이 아니라 state pressure와 support trigger로 취급한다.
- LLM은 표현만 담당한다.
- 로드맵을 확장하기 전에 foundation을 먼저 완성한다.

## 완성 기준

Foundation은 모델이 다음을 할 수 있을 때 완성된다.

- input을 받는다
- emotion을 감지한다
- state를 업데이트한다
- short-term memory를 저장한다
- long-term memory를 요약한다
- Big Five traits를 유지한다
- Dark Tetrad 연구를 안전성 참고로만 사용한다
- MND-N PERMA/Flourish support recommendation을 만든다
- 위기 신호에서 안전 안내로 전환한다
- governance rules를 적용한다
- action을 선택한다
- 중요한 내부 변화를 로그로 남긴다
- LLM이 엔진을 통제하지 않고 NPC로 말하게 한다
