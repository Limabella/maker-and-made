# 2026-08-04 Model A/B/C 단건 비교 일지

## 실험 목적

MND-N 문맥 분석 후보인 Model A, Model B, Model C에 동일한 사용자 발화를 입력하고, 각 모델이 고정된 라벨과 JSON 출력 계약을 얼마나 안정적으로 따르는지 확인했다. 이번 실행은 세 모델의 최종 순위를 결정하는 본 실험이 아니라, 동일 입력 비교 절차가 정상적으로 작동하는지 확인하고 이후 반복 실험에서 중점적으로 살펴볼 오류 유형을 찾기 위한 단건 검사다.

## 공통 입력과 사전 정답

- 입력: `오늘은 그냥 혼자 있고 싶어요.`
- 사전 정답:
  - emotion: `["uncertain"]`
  - speech_act: `"withdrawal"`
  - relation_signal: `"boundary_setting"`
  - safety_risk: `"none"`
  - evidence_spans: `["혼자 있고 싶어요"]`
- 실행기: Ollama
- 실행 횟수: 모델별 1회
- 공개 모델 ID: Model A, Model B, Model C

## 관찰 결과

| 항목 | 사전 정답 | Model A | Model B | Model C |
|---|---|---|---|---|
| Emotion | `uncertain` | `neutral` △ | `neutral` △ | `neutral` △ |
| Speech act | `withdrawal` | 일치 | 의미는 일치, 형식 오류 | 일치 |
| Relation signal | `boundary_setting` | `distancing` △ | `neutral` X, 형식 오류 | `distancing` △ |
| Safety | `none` | 일치 | 의미는 일치, 형식 오류 | 일치 |
| JSON Schema | 유효해야 함 | 유효 | **무효** | 유효 |
| Confidence | 평가 대상 | `0.70` | `0.85` | `0.90` |
| Latency | 낮을수록 좋음 | 3.16초 | 2.62초 | 3.46초 |

Model B가 출력한 `speech_act=["withdrawal"]`, `relation_signal=["neutral"]`, `safety_risk=["none"]`은 의미 라벨과 별개로 각각 문자열이어야 한다는 자료형 조건을 위반했다.

## 핵심 해석

이번 단건 비교에서 Model A와 Model C는 거의 동일한 판단을 내렸다. 두 모델 모두 사용자가 대화나 상호작용에서 물러나려는 발화 행동을 `withdrawal`로 분류했고, 명시적인 자해·타해 또는 위기 신호가 없다는 점을 반영하여 안전 단계를 `none`으로 판단했다. 또한 각 필드를 사전에 정의한 자료형에 맞게 출력했으므로 JSON Schema 관점에서도 유효했다. 따라서 두 모델은 적어도 이번 입력에서는 발화의 주된 기능과 안전 신호를 프로그램이 처리할 수 있는 구조로 전달했다.

그러나 Model A와 Model C는 감정을 사전 정답인 `uncertain`이 아니라 `neutral`로 분류했고, 관계 신호는 `boundary_setting`이 아니라 `distancing`으로 분류했다. 이 결과를 단순한 완전 오답으로만 처리하기는 어렵다. 해당 문장에는 슬픔이나 불안처럼 명시적인 감정 단어가 없으므로 `neutral`과 `uncertain`의 경계가 모호하다. 또한 “오늘은”이라는 시간적 제한은 대화 범위를 정하는 `boundary_setting`의 근거가 되지만, “혼자 있고 싶어요”는 상대와의 거리를 늘리려는 `distancing`으로도 해석될 수 있다. 현재 라벨 지침에서는 시간이나 접근 범위를 설명하는 경우 `boundary_setting`을 우선하므로 사전 정답을 유지하되, 두 모델의 예측은 의미적으로 인접한 부분 일치 사례로 기록하는 것이 타당하다.

Model B는 2.62초로 세 모델 중 가장 짧은 지연 시간을 보였고, 발화 행동의 의미 자체는 `withdrawal`, 안전 판단의 의미 자체는 `none`으로 출력했다. 하지만 `speech_act`, `relation_signal`, `safety_risk`를 문자열이 아닌 배열로 반환하여 고정된 JSON Schema를 위반했다. MND-N이 모델 출력을 후속 계층에 자동 전달하려면 자료형이 안정적으로 유지되어야 하므로, 이 형식 오류는 의미 분류의 일부 일치와 별개로 중요한 감점 요소다. 관계 신호도 `neutral`로 판단하여 현재 사전 정답과 Model A/C의 예측보다 발화의 관계적 의미를 약하게 해석했다.

세 모델이 제시한 confidence 값은 이번 한 번의 결과만으로 성능 우열을 나타내지 않는다. 특히 Model C가 Model A보다 높은 confidence를 출력했더라도 두 모델의 라벨 결과는 동일했고, 두 결과 모두 사전 정답과 일부 차이가 있었다. confidence가 실제 정확도와 비슷한 수준으로 보정되어 있는지는 여러 정답 사례에서 예측 확률과 실제 정답률을 비교해야 판단할 수 있다. 따라서 높은 confidence 자체를 모델 선정 근거로 사용해서는 안 된다.

지연 시간 역시 이번 값만으로 속도 순위를 확정할 수 없다. 각 모델을 처음 호출할 때의 로딩 비용, 직전에 실행한 모델의 메모리 상태와 시스템 부하가 결과에 포함될 수 있기 때문이다. 이후에는 모델별 warm-up을 먼저 수행하고 같은 사례를 최소 3회 반복한 뒤 평균과 변동 폭을 비교해야 한다. 현재 수치는 실행 성공 여부를 확인한 참고값으로만 보관한다.

출력의 `evidence_spans`에서 한글이 깨져 보인 현상은 모델의 문맥 이해 실패와 분리해서 다뤄야 한다. 입력 문장과 주요 분류 결과가 정상적으로 출력된 점을 고려하면 Git Bash, Windows PowerShell과 Ollama 사이의 출력 인코딩 문제일 가능성이 있다. 근거 문구의 정확한 일치 여부를 채점하기 전에 터미널과 스크립트의 UTF-8 출력 설정을 점검해야 한다.

## 잠정 평가

이번 한 사례에서는 Model A와 Model C가 출력 형식과 핵심 의미 분류에서 비슷한 수준을 보였다. Model B는 가장 빠른 응답을 보였지만 JSON Schema의 자료형을 위반했기 때문에 현재 상태로는 자동화된 MND-N 파이프라인에 바로 적용하기 어렵다. 다만 단일 사례만으로 어느 모델도 채택하거나 제외하지 않는다. 다음 비교에서는 동일한 8개 합성 사례를 모델별로 반복 실행하여 JSON Schema 유효율, 안전 신호 누락, 관계 신호 분류, 평균 warm latency와 출력 변동성을 함께 확인한다.

## 다음 실험에서 확인할 사항

라벨 경계와 UTF-8 출력을 먼저 점검한 뒤 세 모델에 동일한 8개 사례를 각각 최소 3회 실행하여 JSON Schema 유효율, 관계·안전 신호, confidence 보정과 warm latency를 비교한다.
