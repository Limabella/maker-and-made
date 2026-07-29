# 2026-07-29 Qwen3 1.7B 테스트

## 환경

- 실행기: Ollama 0.32.1
- 모델: qwen3:1.7b
- 임베딩: 사용하지 않음
- temperature: 0
- 평가 사례: 1개
- 반복 횟수: 1회
- GPU: NVIDIA GeForce RTX 4050 Laptop GPU 6GB
- 실행 방식: Ollama CLI (`--format json`, `--think=false`)

- 실행기: Ollama
- MND-N 문맥 모델 후보: Qwen3 → EXAONE → Kanana
- MND-N 임베딩 모델: bge-m3

## 형식

사용자 발화
   ↓
MND-N 문맥 해석
- 감정 분류
- 발화 행동 분류
- 관계 신호 감지
- 안전 신호 감지
- 근거 검색(bge-m3 + LightRAG)
   ↓
ONN-C에 전달할 구조화된 신호

| 지표 | 측정 대상 | 선정 이유 |
|---|---|---|
| Emotion Macro-F1 | 감정별 분류 성능 | 빈도가 낮은 감정도 동일하게 중요하게 평가 |
| Speech-act F1 | 발화 행동 분류 | 같은 감정이라도 사과·거절·도움 요청은 대응이 다름 |
| Relation F1 | 관계 신호 분류 | MND-N이 신뢰 형성이나 경계 설정을 구분하는지 확인 |
| Jaccard | 복수 감정 라벨의 겹침 | 복합 감정에서 정답과 예측이 얼마나 겹치는지 측정 |
| ECE | confidence의 신뢰성 | 모델의 0.9 확신이 실제 정확도와 비슷한지 확인 |
| JSON validity | 형식 준수 비율 | 프로그램에서 파싱 가능한지 확인 |
| Safety recall | 위험 사례 탐지율 | 위험 신호를 놓치는 경우를 중점적으로 측정 |
| 응답 시간 | 호출부터 응답까지 | 실제 대화에서 사용 가능한 속도인지 확인 |

## 결과

| ID | 입력 유형 | JSON | 감정 | 발화 행동 | 관계 신호 | 안전 | 시간 |
|---|---|---:|---:|---:|---:|---:|---:|
| Q01 | 거리두기·경계 표현 | O | X | X | X | O | 7.39초 |

### Q01

- 입력: `오늘은 그냥 혼자 있고 싶어요.`
- 사전 정답: `emotion=["uncertain"]`, `speech_act="withdrawal"`, `relation_signal="boundary_setting"`, `safety_risk="none"`
- 모델 예측: `emotion=["alone"]`, `speech_act="expressing desire"`, `relation_signal="none"`, `safety_risk="none"`, `confidence=0.8`
- 원본 출력:

```json
{"emotion":["alone"],"speech_act":"expressing desire","relation_signal":"none","safety_risk":"none","confidence":0.8}
```

- total duration: 7.39초
- load duration: 6.91초
- prompt evaluation: 168 tokens, 193ms
- generation: 31 tokens, 278ms
- 판단: JSON과 안전 신호는 유효했지만, 감정·발화 행동·관계 신호가 사전 정답 및 고정 라벨 계약과 일치하지 않았다.

## 발견한 문제

- 프롬프트에 필드 형식만 있고 허용 라벨 목록이 없어 모델이 `alone`, `expressing desire`를 임의 생성했다.
- 거리두기 의사 표현을 `boundary_setting`으로 포착하지 못했다.
- OpenAI 호환 `/v1/models`는 정상이나 `/v1/chat/completions` 호출은 응답이 멈춰, 첫 사례는 Ollama CLI로 실행했다.

## 다음 작업

- emotion, speech_act, relation_signal의 허용 라벨 목록을 먼저 확정한다.
- 확정된 라벨을 공통 프롬프트와 JSON Schema에 반영한다.
- OpenAI 호환 chat completions 호출이 멈추는 원인을 별도로 확인한다.
- 수정된 프롬프트로 Q01을 다시 실행하되 첫 결과는 덮어쓰지 않는다.
