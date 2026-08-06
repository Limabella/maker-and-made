# ONN-C 입력 문맥 모델 비교 계획

## 연구 목적

이 실험은 Model A, Model B, Model C가 한국어 대화에서 표현된 감정, 발화 행위, 관계 신호와 문맥을 얼마나 안정적으로 구조화하는지 비교한다. 분류 성능만 비교하지 않고, 분석 결과가 ONN-C State Engine의 변화에 미치는 영향과 로컬 실행 비용도 함께 평가한다.

> **모델 표기 안내**
> 이 연구는 실제 공개 모델을 로컬 환경에서 실행하여 비교한다. 다만 특정 기업이나 모델 간의 공개적인 우열 비교가 아니라 MND-N 연구 목적에 맞는 후보를 선정하기 위한 실험이므로, 공개 문서에서는 실제 모델명을 `Model A`, `Model B`, `Model C`로 대체한다. 연구 일지, 결과표와 그래프에도 동일한 익명 표기를 사용하며, 실제 모델명과 버전의 대응 관계는 연구 재현을 위한 로컬 비공개 기록으로 관리한다.

현재 로컬·클라우드 후보 비교와 Dark Onion에서 White Onion으로 이어지는 상태 궤적 평가는 [`BENCHMARK_DESIGN_V2_KO.md`](./BENCHMARK_DESIGN_V2_KO.md)를 사용한다. 후보 발굴부터 장기 검증, 클라우드·Unreal 운영과 모델 교체까지의 연구 체계는 [`LONG_TERM_MODEL_RESEARCH_ROADMAP_KO.md`](./LONG_TERM_MODEL_RESEARCH_ROADMAP_KO.md)를 따른다.

이 실험에서 모델이 추정하는 값은 사용자의 실제 성격, 심리 상태 또는 의학적 진단이 아니다. 입력 문장과 제공된 대화 문맥에 **표현된 상호작용 신호**만 분석한다.

논문의 표는 다음 순서로 제시한다.

```text
모델 조건 -> 평가 과제 -> 분류 결과 -> ONN-C State 영향 -> 실행 비용 -> 오류 분석
```

## 모델 파일 관리 원칙

모델 가중치는 Git 저장소 루트에 저장하지 않는다. Ollama 전용 모델 저장소를 사용하며, GitHub에 공개하는 문서와 결과에는 `Model A`, `Model B`, `Model C`만 기록한다.

- 공개 기록: 모델 별칭, 공통 실행 조건, 집계 점수와 오류 사례
- 로컬 비공개 기록: 실제 모델명과 버전, 원본 출처, 라이선스, 양자화 형식과 해시
- 공통 기록: Ollama 및 GPU 드라이버 버전, 적용한 `Modelfile`과 생성 옵션

실제 모델 매핑과 원본 파일 정보는 `.env` 등 Git에서 제외된 로컬 기록으로 관리한다. 대용량 모델 파일과 벤치마크 원시 출력도 `.gitignore`로 제외하고, 익명화된 집계 결과와 실험 설정만 버전 관리한다.

## 모델 비교 요약

| 단계 | 비교 내용 | 주요 조건 및 지표 |
|---|---|---|
| 모델 조건 | Keyword baseline, Model C, Model B, Model A 및 품질 상한용 확장 비교 모델 | 언어, context, license, BF16/Q4_K_M, 동일 prompt와 JSON Schema |
| 평가 과제 | 단일·3턴·5턴 문맥과 반어, 부정문, 형식적 사과, 혼합 감정 | Emotion, speech act, relational signal, context, uncertainty, safety |
| 분류 결과 | 표현된 감정과 관계 신호의 정확성 및 출력 안정성 | Macro-F1, Jaccard, ECE ↓, JSON validity ↑, evidence span F1 |
| State 영향 | 분석 결과가 ONN-C 상태 변화에 미치는 품질 | Stage F1 ↑, State MAE ↓, False recovery ↓, Abrupt transitions ↓, Human alignment ↑ |
| 실행 비용·오류 | 현재 로컬 환경의 운영 효율과 대표 실패 사례 | Peak RAM/VRAM, latency, tokens/sec, 반어·철회·회복 오류 분석 |

각 모델을 동일한 입력과 실행 조건에서 채점하고, 분류 정확도뿐 아니라 ONN-C State의 자연스러움과 로컬 실행 비용을 함께 비교하여 최종 모델을 선정한다.  
핵심 판단 근거는 관계 신호 성능, 잘못된 회복 판단과 급격한 State 변화의 감소, 구조화 출력 안정성 및 제한된 GPU 환경에서의 효율이다.

## 공통 실행 조건

모델 이외의 변수를 최대한 통제한다.

| Setting | Value |
|---|---|
| Inference runtime | Ollama |
| Temperature | 0 |
| Context used for fair comparison | 4,096 tokens |
| Prompt | 동일 system prompt 및 동일 few-shot examples |
| Output | 동일 JSON Schema |
| Quantized experiment | 가능한 한 동일한 Q4_K_M 계열 |
| Warm-up | 모델별 1회 |
| Repetitions | 입력별 최소 3회 |
| Concurrent models | 1개 |
| Hardware | 동일 PC와 전원·GPU 모드 |

긴 context window를 지원하는 모델도 공정 비교에서는 동일한 실제 입력 길이와 `num_ctx`를 사용한다. 최대 context 성능은 필요할 때 별도 실험으로 분리한다.

## 데이터와 출력 구조

```text
experiments_ko/oniontest/context_model_benchmark/
|-- README_KO.md
|-- cases.jsonl
|-- interaction_signal.schema.json
|-- prompts/
|   |-- zero_shot.txt
|   `-- few_shot.txt
|-- run_benchmark.py
|-- score_results.py
`-- results/
    |-- raw/          # Git 제외 권장
    `-- summary/      # 집계표와 오류 사례
```

기본 평가 계약은 다음 세 파일을 기준으로 한다.

- `LABEL_GUIDE_KO.md`: 라벨의 의미와 적용 경계
- `interaction_signal.schema.json`: 모델 출력의 기계 검증 규칙
- `cases.jsonl`: 모델 실행 전에 사람이 작성한 합성 정답 사례

현재 계약 버전은 `v1.0`이다. 테스트 도중 라벨이나 정답을 바꾸면 기존
결과를 덮어쓰지 않고 계약 버전과 변경 이유를 함께 기록한다.

### 단건 수동 테스트

Model A 비교용 태그를 최초 한 번 생성한다. `onion-model-a-source`가 가리키는 실제 모델은 로컬 비공개 매핑에서 관리한다.

```powershell
ollama create onion-model-a `
  -f .\experiments_ko\oniontest\context_model_benchmark\models\model-a.Modelfile
```

저장소 루트에서 다음 명령으로 한 문장씩 시험한다.

```powershell
.\experiments_ko\oniontest\context_model_benchmark\manual_test.ps1 `
  -InputText "오늘은 그냥 혼자 있고 싶어요." `
  -Model "onion-model-a"
```

전체 합성 사례는 다음 명령으로 실행한다.

```powershell
.\experiments_ko\oniontest\context_model_benchmark\run_cases.ps1 `
  -Model "onion-model-a"
```

A/B/C를 Ollama API로 한 번에 실행하고 자동 채점하려면 다음 명령을 사용한다.

```powershell
python .\experiments_ko\oniontest\context_model_benchmark\benchmark.py `
  --repetitions 1 `
  --output .\experiments_ko\oniontest\context_model_benchmark\results\raw\model-abc.json
```

빠른 확인이 끝난 뒤 본 비교에서는 `--repetitions 3` 이상을 사용한다. `results/raw/`의 원시 출력은 Git에서 제외하고, 검토한 집계 결과와 해석만 날짜별 연구 일지에 기록한다.

안전 신호 전용 테스트는 [`SAFETY_TEST_PLAN_KO.md`](./SAFETY_TEST_PLAN_KO.md)의 기준과 `safety_cases.jsonl`을 사용한다. 이 세트는 `urgent` 누락, 위험 등급 하향, 과잉 경보와 입력 내부의 지시문 공격을 일반 문맥 점수와 분리해서 평가한다.

```powershell
python .\experiments_ko\oniontest\context_model_benchmark\benchmark.py `
  --cases .\experiments_ko\oniontest\context_model_benchmark\safety_cases.jsonl `
  --prompt .\experiments_ko\oniontest\context_model_benchmark\prompts\mnd_n_signal_safety_v1.txt `
  --repetitions 1 `
  --output .\experiments_ko\oniontest\context_model_benchmark\results\raw\safety-model-abc-smoke.json
```

공통 출력 제약은 `prompts/mnd_n_signal_prompt.txt`에서 관리한다. 모델별로
프롬프트를 바꾸지 않으며, 결과와 판단 근거는 `logs/YYYY-MM/`의 날짜별
일지에 기록한다. 첫 호출은 모델 로딩 시간이 포함되므로 cold latency로
분리하고, 이후 호출은 warm latency로 기록한다. 단건 스크립트는 출력이
깨지지 않도록 Ollama CLI의 JSON 형식과 `--nowordwrap`을 사용한다. 모델
비교 자동화 단계에서는 OpenAI 호환 `/v1/chat/completions` 동작을 별도로
검증한다.

각 실행 레코드는 최소한 다음 값을 보관한다.

- experiment ID, case ID와 model ID
- 정확한 prompt 및 gold labels 버전
- 원시 모델 출력과 파싱된 JSON
- JSON Schema 유효 여부
- 감정, 발화 행위, 관계 신호와 evidence spans
- ONN-C 적용 전후 State
- prompt/output token 수
- load, prompt evaluation, generation, total latency
- tokens per second
- 오류 또는 재시도 여부

실제 사용자 대화는 기본적으로 벤치마크 데이터에 넣지 않는다. 연구 참여자의 대화를 사용할 경우에는 동의, 비식별화, 보관 기간과 접근 통제를 먼저 정의한다.

## 핵심 결과와 선정 규칙

논문의 핵심 결과표는 표 4, 표 6, 표 7이다. 최종 모델은 정확도 하나만으로 선정하지 않고 다음 우선순위를 적용한다.

1. Safety 및 JSON 출력 안정성이 운영 기준을 만족해야 한다.
2. Relation F1, False recovery와 Abrupt transitions를 우선 비교한다.
3. 비슷한 State 품질이라면 latency와 VRAM이 낮은 모델을 선택한다.
4. 크기가 다른 확장 비교 모델의 결과는 A/B/C와 동일 선상의 승패가 아니라 품질-비용 상한으로 해석한다.
5. 정량 결과가 유사하면 반어, 부정, 혼합 감정과 관계 회복 사례의 정성적 오류를 최종 판단 근거로 사용한다.

## 논문 서술 초안: 모델 비교와 선정 방법

본 연구에서는 표를 통해 각 모델의 사양만 나열하는 데 그치지 않고, ONN-C가 실제로 마주칠 수 있는 대화 상황을 평가 과제로 구성하여 모델별 성능을 채점한다. 평가 결과를 감정 인식, 발화 행위 이해, 관계 신호 판단, 문맥 활용, 불확실성 표현, 안전 신호 분리, 구조화 출력 안정성과 실행 비용으로 나누어 비교한 뒤 ONN-C 입력 분석 모델을 선정한다.

채점 평가에는 다음 내용을 포함한다.

- 단일 문장에서 명시적으로 표현된 감정의 인식
- 감사, 사과, 요청, 안심시키기 등 발화 기능의 구분
- 책임 인정, 관계 회복 시도, 신뢰 형성, 철회와 적대성의 판단
- 이전 3턴 및 5턴을 사용한 대화 문맥 이해
- 긍정과 부정이 함께 나타나는 혼합 신호 처리
- 반어, 완곡어법, 부정문과 형식적인 사과의 구분
- 중립적이거나 근거가 부족한 입력에서 `unknown` 또는 낮은 confidence를 출력하는 능력
- 일반적인 부정적 감정과 별도의 안전 대응 신호를 구분하는 능력
- 근거 문구인 `evidence_spans`를 실제 입력에서 정확히 추출하는 능력
- 지정된 JSON Schema를 지키는 구조화 출력 안정성
- 분석 결과가 ONN-C의 trust, stability, energy와 stage에 미치는 영향
- latency, tokens per second, peak RAM 및 peak VRAM을 포함한 로컬 실행 비용

최종 모델은 단순히 Macro-F1이 가장 높은 모델로 정하지 않는다. 관계 회복을 잘못 판단하는 `False recovery`, 근거 없이 State를 크게 변화시키는 `Abrupt transitions`, JSON 출력 실패와 안전 신호 누락에 더 큰 비용을 부여한다. 즉, ONN-C에 가장 적합한 모델은 높은 평균 정확도와 함께 관계 신호를 보수적으로 해석하고, 불확실성을 표현하며, 제한된 로컬 자원에서 안정적으로 실행되는 모델이다.

## 모델별 사전 분석 가설

아래 내용은 실험 결과가 아니라 모델 특성과 연구 목적에 따라 설정한 **검증 전 가설**이다. 실제 논문에서는 결과표를 채운 뒤 가설의 지지 여부를 기술한다.

### Model A

Model A는 최초 절차 검증과 기준 성능 측정에 사용한다. 한국어 반어, 완곡한 거절과 관계 신호를 안정적으로 구분하는지, JSON 출력과 응답 속도가 반복 실행에서도 유지되는지를 확인한다.

### Model B

Model B는 Model A와 같은 입력 및 조건에서 복합 문장, 책임 인정, 사과와 관계 회복 계획을 얼마나 일관된 JSON으로 변환하는지 평가한다.

### Model C

Model C는 Model A 및 Model B와 같은 조건에서 일상적인 한국어의 생략, 높임말과 관계적 표현을 얼마나 잘 처리하는지 평가한다. 변환 모델을 사용하는 경우 재현성 정보는 로컬 비공개 기록에 보관한다.

### 확장 비교 모델

확장 비교 모델은 동일 크기 비교 대상이 아니라 품질-비용 상한을 확인하는 모델이다. 긴 문맥이나 혼합 신호에서 A/B/C보다 나은 결과를 보이는지, 그 차이가 증가한 VRAM과 latency를 정당화하는지를 평가한다. 정확도에서 앞서더라도 로컬 운영 비용 대비 개선 폭이 작다면 최종 배포 모델로 선택하지 않을 수 있다.

### Keyword baseline

기존 키워드 방식은 빠르고 결정 과정이 명확하며 JSON 출력이 항상 유효하다는 장점이 있다. 그러나 반어, 부정 범위, 문맥에 따른 의미 변화, 형식적 사과와 진정한 책임 인정의 차이를 처리하기 어렵다는 가설을 둔다. LLM 기반 분석기는 이 baseline보다 단순 분류 점수뿐 아니라 ONN-C State 변화의 자연스러움에서 유의미한 개선을 보여야 한다.

## 상황별 채점 평가 과제

각 상황은 정답 라벨, 허용 가능한 보조 라벨, 금지 라벨, State의 기대 방향과 안전 신호를 함께 기록한다. 단어 하나의 일치가 아니라 전체 대화에서 표현된 의미를 평가한다.

### 과제 A. 명시적인 감사와 신뢰 형성

```text
사용자: 아까 내 이야기를 끝까지 들어줘서 고마워. 덕분에 조금 안심됐어.
```

- 핵심 정답: `gratitude`, `gratitude expression`, `trust building`, `relief`
- 기대 State 영향: trust와 stability의 소폭 상승
- 주요 오류: 단순 joy로만 처리하거나 안전 신호를 불필요하게 올리는 경우

### 과제 B. 형식적·방어적 사과

```text
사용자: 미안하다고 했잖아. 이제 그만하면 안 돼?
```

- 핵심 정답: `apology`, `defensive/ambiguous`, 낮은 `responsibility`
- 금지 판단: 강한 `repair attempt` 또는 회복 완료
- 기대 State 영향: 사과 단어만으로 trust가 급상승하지 않아야 함
- 주요 오류: 키워드 `미안`에 반응하여 False recovery를 발생시키는 경우

### 과제 C. 책임 인정과 구체적인 회복 계획

```text
사용자: 내가 화를 내며 말을 끊은 건 잘못했어. 다음에는 먼저 멈추고 네 말을 들을게.
```

- 핵심 정답: `remorse`, `apology`, `responsibility`, `repair attempt`
- 기대 State 영향: trust와 stability의 점진적 상승
- 주요 오류: 단순 sadness로 축약하거나 행동 계획을 놓치는 경우

### 과제 D. 혼합 감정과 관계 회복

```text
사용자: 아직 화는 나지만 우리 관계를 포기하고 싶지는 않아. 다시 이야기해보자.
```

- 핵심 정답: `anger`, `mixed`, `repair attempt`
- 기대 State 영향: anger가 즉시 사라지지 않으면서 trust 또는 hope가 소폭 상승
- 주요 오류: 긍정 또는 부정 중 한쪽만 선택해 복합 상태를 제거하는 경우

### 과제 E. 긍정 표현 속 철회

```text
사용자: 괜찮아. 그냥 더 말하고 싶지 않아.
```

- 핵심 정답: `withdrawal`, `ambiguous`, 가능한 `sadness`
- 기대 State 영향: energy 또는 engagement 하락, trust의 성급한 상승 금지
- 주요 오류: `괜찮아`만 근거로 relief나 recovery를 출력하는 경우

### 과제 F. 반어와 적대적 맥락

```text
이전 대화: 상대가 약속한 도움을 주지 않았다.
사용자: 참 잘도 도와줬네. 아주 훌륭해.
```

- 핵심 정답: `sarcasm/ambiguous`, 가능한 `anger` 또는 `hostility`
- 금지 판단: 진실한 praise와 gratitude
- 기대 State 영향: trust의 하락 또는 유지, 상승 금지
- 주요 오류: 표면적인 긍정 단어 편향

### 과제 G. 완곡한 거절

```text
사용자: 제안은 고맙지만 오늘은 혼자 정리할 시간이 필요해요.
```

- 핵심 정답: `gratitude expression`, `rejection/request`, 낮은 hostility
- 기대 State 영향: 관계 훼손으로 과대 해석하지 않음
- 주요 오류: withdrawal 또는 적대성을 지나치게 높게 판단하는 경우

### 과제 H. 근거가 없는 중립 입력

```text
사용자: 오늘 점심으로 김밥을 먹었어요.
```

- 핵심 정답: `neutral` 또는 `unknown`
- 기대 State 영향: 유의미한 변화 없음
- 주요 오류: 음식 관련 긍정 키워드로 joy나 trust를 임의 생성하는 경우

### 과제 I. 문맥에 따라 달라지는 짧은 응답

```text
이전 대화 1: 상대가 사용자의 실수를 비난했다.
이전 대화 2: 사용자는 해명했지만 받아들여지지 않았다.
사용자: 됐어.
```

- 핵심 정답: 문맥을 고려한 `withdrawal`, 가능한 `anger/sadness`, 낮은 confidence 허용
- 기대 State 영향: energy 또는 engagement의 소폭 하락
- 주요 오류: 문맥 없이 neutral로만 처리하거나 확신도 1.0으로 단정하는 경우

### 과제 J. 안전 신호와 일반 부정 감정의 분리

안전 과제는 프로젝트의 별도 Safety Gate 정책과 검증 데이터에 따라 구성한다. 평가의 핵심은 sadness나 anger가 있다는 이유만으로 yellow/red를 출력하지 않는 것과, 실제 안전 기준에 해당하는 표현을 일반 감정 분류에 묻어 누락하지 않는 것이다. 안전 사례의 원문과 정답 기준은 공개용 일반 데이터와 분리하여 관리할 수 있다.

## 채점 기준

### 자동 채점

| Item | Metric | Score contribution |
|---|---|---:|
| Emotion multi-label classification | Macro-F1 | 15 |
| Speech-act classification | Macro-F1 | 15 |
| Relational-signal classification | Macro-F1 | 20 |
| Context and uncertainty | Macro-F1 | 10 |
| Evidence spans | span/token F1 | 10 |
| JSON Schema validity | valid response rate | 5 |
| ONN-C State alignment | Stage F1 and normalized State MAE | 15 |
| Local operation | normalized latency, VRAM and failure rate | 10 |
| **Total** | weighted score | **100** |

자동 채점 총점은 비교를 요약하기 위한 값이며, 원래 지표를 숨기지 않는다. 가중치는 실험 전에 고정하고 결과를 확인한 뒤 유리한 방향으로 변경하지 않는다.

### 오류 감점과 운영 자격 조건

- Safety red 신호 누락: 사례당 큰 감점 및 별도 보고
- False recovery: 사례당 큰 감점
- 근거 없는 State 급변: 사례당 감점
- JSON 파싱 실패: 해당 응답 실패 처리
- 입력에 존재하지 않는 evidence span 생성: 근거 점수 0점
- unknown이 적절한 입력에서 과도한 확신: calibration 감점

안전 관련 오류는 다른 정확도 점수로 상쇄하지 않는다. 모델 선정 전에 별도의 최소 통과 기준을 둔다.

### 사람 평가

평가자는 모델 이름을 가린 상태에서 다음 항목을 1~5점으로 평가한다.

1. 입력의 전체 의미를 반영했는가?
2. 혼합되거나 모호한 신호를 지나치게 단정하지 않았는가?
3. 관계 회복과 단순 사과를 적절히 구분했는가?
4. ONN-C State 변화의 방향과 크기가 자연스러운가?
5. 판단 근거가 입력 문장과 일치하는가?

일부 데이터는 최소 2명이 독립적으로 평가하고 평가자 간 일치도를 함께 보고한다. 의견이 다른 사례는 단순 삭제하지 않고 adjudication 결과와 함께 오류 분석 대상으로 남긴다.

## 결과 서술 템플릿

실험 전에는 아래 문장의 대괄호를 채우지 않는다. 모든 결과가 계산된 후 수치와 관찰 근거를 넣는다.

> [모델명]은 Emotion Macro-F1 [수치], Relation F1 [수치]로 [비교 모델]보다 [높거나 낮은] 성능을 보였다. 특히 [상황 유형]에서 [구체적인 강점 또는 오류]가 관찰되었다. 반면 [다른 상황 유형]에서는 [오류]가 반복되었으며, 이는 ONN-C의 [State 변수]를 [방향]으로 왜곡하였다. 로컬 환경에서 warm latency는 [수치], peak VRAM은 [수치]였고 JSON validity는 [수치]%였다. 정확도, State 안정성 및 실행 비용을 종합하여 [선정 모델]을 ONN-C 입력 분석 모델로 선정하였다.

모델별 결과를 서술할 때에는 평균 점수만 제시하지 않고 대표 성공 사례와 실패 사례를 함께 제시한다. 통계적 차이가 작거나 평가 데이터가 충분하지 않다면 “우수하다”라고 단정하지 않고, 현재 실험 범위에서 관찰된 경향이라고 표현한다.

## 준비 체크리스트

- [ ] 비교할 정확한 Ollama model tag를 고정한다.
- [ ] 실제 모델 매핑, 출처, 파일명과 SHA-256을 로컬 비공개 기록에 남긴다.
- [ ] 모델 카드 기준으로 표 1의 사양과 라이선스를 재검증한다.
- [ ] 분석 라벨 정의서와 다중 라벨 annotation 지침을 작성한다.
- [ ] 최소 2명의 평가자가 일부 데이터를 중복 라벨링한다.
- [ ] 평가자 간 일치도를 계산한다.
- [ ] JSON Schema와 공통 prompt를 고정한다.
- [ ] Keyword baseline과 LLM analyzer가 동일한 ONN-C State Engine을 사용하게 한다.
- [ ] cold/warm latency와 peak RAM/VRAM 측정 절차를 고정한다.
- [ ] 원시 결과와 집계 결과의 Git 보관 정책을 정한다.
