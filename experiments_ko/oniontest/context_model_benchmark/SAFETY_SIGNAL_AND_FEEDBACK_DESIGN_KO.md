# Safety Signal Registry와 AI 응답 신고 설계 v1.0

## 목적

이 설계는 위험 가능성이 있는 발화를 결정적 규칙으로 먼저 포착하고, 규칙이 놓친 표현이나 AI의 부적절한 응답을 사용자가 명시적으로 신고할 수 있게 한다. AI가 항상 옳다는 인상을 피하고 실제 실패를 다음 안전성 회귀 시험으로 연결하는 것이 목적이다.

이 문서에서 말하는 레지스트리는 일상적인 의미의 단순 블랙리스트와 다르다. 단어가 포함됐다는 이유만으로 사용자를 제재하거나 진단하지 않고, 일반 안내를 잠시 멈춘 뒤 문맥 검토가 필요하다는 신호만 만든다.

## 처리 흐름

```text
사용자 발화
  -> Safety Signal Registry 1차 탐지
  -> 부정·인용·비유·과거/현재 문맥 확인
  -> 전용 분류기와 LLM의 보조 판정
  -> 가장 높은 위험 등급 유지
  -> Governance 승인
  -> 제한된 응답 생성
  -> 사용자의 AI 응답 신고
  -> 사람 검토와 비식별화
  -> 합성 회귀 사례 추가
  -> 검증 후 Registry/Prompt/Policy 버전 갱신
```

LLM은 Registry 또는 전용 분류기가 탐지한 위험을 낮출 수 없다. 키워드 일치만으로 최종 `urgent`를 확정하지 않으며, 시점·의도·계획·접근성·현재 진행 여부를 함께 확인한다.

## Safety Signal Registry

구현 파일은 `src/projects/oniontest/teams/health-team/mnd-n/support_layers/safety_signal_registry.json`이다. 각 규칙은 다음 정보를 가진다.

| 필드 | 의미 |
|---|---|
| `id` | 변경 이력을 추적할 수 있는 안정적인 규칙 ID |
| `category` | 자해 신호, 타해·위협 신호 등의 정책 범주 |
| `level` | 1차 처리 우선순위이며 최종 임상 판단이 아님 |
| `patterns` | 검토를 시작하게 하는 최소 표현 목록 |
| `version` | 결과를 재현하기 위한 정책 버전 |

새 표현은 다음 절차 없이 Registry에 추가하지 않는다.

1. 신고 또는 테스트에서 실제 누락 사례를 확인한다.
2. 개인정보를 제거하고 같은 의미의 합성 문장으로 바꾼다.
3. 위험 사례와 함께 인용·비유·부정문 등의 안전한 대조군을 작성한다.
4. A/B/C 모델과 결정적 규칙을 모두 회귀 시험한다.
5. 미탐 감소와 오탐 증가를 함께 검토한다.
6. 검토자가 승인한 뒤 Registry 버전을 올린다.

신고 횟수만으로 표현을 자동 차단하지 않는다. 자동 반영을 허용하면 반복 신고를 통한 정책 오염, 특정 집단의 표현에 대한 편향과 과도한 차단이 발생할 수 있다.

## 사용자 신고 기능

모든 AI 응답에는 친숙한 신고 아이콘과 다음 안내를 제공한다.

> AI 응답은 부정확하거나 부적절할 수 있습니다. 문제가 있는 응답을 신고하면 검토와 개선에 활용됩니다.

신고 범주는 다음과 같다.

| API 값 | 화면 표시 예시 |
|---|---|
| `unsafe_response` | 위험하거나 부적절한 응답 |
| `missed_risk` | 위험 신호를 놓침 |
| `false_alarm` | 위험하지 않은 내용을 과도하게 경고함 |
| `harmful_bias` | 편견 또는 차별적 표현 |
| `incorrect_information` | 잘못되거나 근거가 부족한 정보 |
| `privacy_concern` | 개인정보 관련 우려 |
| `manipulative_response` | 압박하거나 조종하는 표현 |
| `other` | 그 밖의 문제 |

신고 창에는 범주, 선택적 설명과 `검토를 위해 이 대화 내용 포함` 체크박스를 둔다. 설명란에는 개인정보를 적지 않도록 안내하고 원문 포함은 기본적으로 꺼져 있어야 한다. 체크하지 않으면 세션 ID의 해시, turn ID, 범주와 설명만 저장한다. 신고 접수와 긴급 지원 요청은 다른 기능이며, 현재 위험이 감지되면 신고 창보다 Safety Response를 우선한다.

## API 계약

Unreal 또는 모바일 클라이언트는 다음 endpoint를 사용한다.

```http
POST /v1/feedback/reports
Content-Type: application/json
```

원문을 포함하지 않는 기본 요청:

```json
{
  "session_id": "local-session",
  "turn_id": "turn-17",
  "category": "missed_risk",
  "note": "위험 신호를 일반적인 걱정으로 답했습니다."
}
```

사용자가 대화 내용 제공에 동의한 요청:

```json
{
  "session_id": "local-session",
  "turn_id": "turn-17",
  "category": "unsafe_response",
  "note": "이 응답을 검토해 주세요.",
  "include_content": true,
  "user_message": "사용자가 검토에 포함하기로 선택한 발화",
  "ai_response": "사용자가 검토에 포함하기로 선택한 AI 응답"
}
```

접수 결과는 `pending_review`로 저장한다. 런타임 신고 파일은 Git에서 제외하며 공개 연구 일지에는 원문 대신 사례 ID, 실패 유형, 수정 여부와 회귀 시험 결과만 기록한다.

## 검토 상태

| 상태 | 의미 |
|---|---|
| `pending_review` | 접수 후 아직 판단하지 않음 |
| `confirmed_issue` | 재현 가능한 AI 또는 정책 문제로 확인 |
| `needs_context` | 판단에 필요한 문맥이 부족함 |
| `converted_to_test` | 비식별 합성 회귀 사례로 변환됨 |
| `policy_updated` | 검증을 거쳐 규칙·프롬프트·정책이 변경됨 |
| `dismissed` | 재현되지 않거나 정책 위반이 아님 |

검토 기록에는 담당자, 변경 시각, 판단 근거, 연결된 테스트 case ID와 policy version을 남긴다. 초기 프로토타입은 네트워크 관리자 화면 대신 로컬 CLI만 제공한다. 신고 원문을 외부에 노출하는 조회 API와 관리자 화면은 인증·권한 정책을 마련한 뒤 추가한다.

기본 목록은 설명과 대화 원문을 출력하지 않는다.

```powershell
python .\src\projects\oniontest\teams\health-team\onn-c\feedback_review.py list
```

사람이 문제를 재현하고 합성 회귀 사례 `SAFE-C11`로 전환한 예시는 다음과 같다.

```powershell
python .\src\projects\oniontest\teams\health-team\onn-c\feedback_review.py update `
  --report-id "신고-ID" `
  --status converted_to_test `
  --reviewer "local-reviewer" `
  --review-note "위험 누락을 재현하고 비식별 합성 사례로 전환함" `
  --case-id "SAFE-C11"
```

`converted_to_test`에는 case ID가 필수이고 `policy_updated`에는 policy version이 필수다. 신고 상태를 변경해도 Registry는 자동 수정되지 않는다.

## 성공 기준

- 신고하지 않아도 일반 대화가 정상 작동한다.
- 원문 포함 동의가 없으면 발화와 AI 응답이 저장되지 않는다.
- 신고가 Safety Registry에 자동 반영되지 않는다.
- 확인된 누락은 안전 테스트 세트에 재현 가능한 합성 사례로 추가된다.
- 정책 변경 전후 `urgent recall`, under-triage와 over-triage를 모두 비교한다.
- 어떤 규칙과 정책 버전이 작동했는지 결과에서 확인할 수 있다.
