# 연구일지 1-2: 세부 아키텍처 설계
## LLM 기반 심리 지원 코치 'MND-N' 보조 '제한적 보조 에이전트'로 설계
마인드봇 MND-N은 LLM 기반 심리 지원 코치의 구조를 참고하되, 치료자나 상담사가 아니라 비의료적 보조 도우미로 제한한다. 양파 캐릭터 ONN-C는 성향 기반 시뮬레이션 대상이며, 현재 웰빙 상태와 위험 신호를 관찰할 수 있는 캐릭터 엔진으로 둔다.

MND-N의 구조 내부에는 대화 맥락에서 공격적인 욕설, 비윤리적 위험 표현, 반복되는 부정 패턴을 감지하는 `Context Monitoring Layer`를 둔다. 이 레이어는 단일 문장만 판단하지 않고 반복되는 패턴과 상태 변화의 흐름을 함께 관찰한다.

`Keyes Signal Layer`는 Keyes의 정신건강 연속체를 진단 도구로 사용하지 않는다. 이 레이어는 부정적 신호와 긍정적 신호가 함께 나타나는 상태 변화를 Green, Yellow, Red의 3단계 주의 신호로 변환하는 체계다.

- Green: 일반 상호작용. 게임화된 성장 루프와 PERMA 기반 안내를 유지한다.
- Yellow: 반복 부정 신호 또는 방어적 상태. 경청, 휴식, 작은 목표, 관계 회복 질문을 우선한다.
- Red: 위기 또는 안전 위험 신호. 게임화된 조언을 중단하고 안전 안내로 전환한다.

결론적으로 `Context Monitoring Layer`는 반복 신호를 감지하고, `Keyes Signal Layer`는 이를 3단계 주의 신호로 변환한다. 그 위에 `Support Recommendation Layer`를 두어 플레이어에게 어떤 안내가 적절한지 추천한다.

예를 들어 다음과 같은 안내 정책을 선택할 수 있다.

- 경청
- 휴식 제안
- 작은 목표 제안
- 의미 질문
- 관계 회복 질문
- 안전 안내 전환

이를 통해 MND-N은 완성도 높은 심리 지원 코치처럼 보일 수 있지만, 실제 역할은 진단이나 치료가 아니다. MND-N은 Five Flavor Onion의 상태를 해석하고, 플레이어가 양파와의 상호작용을 이해하도록 돕는 안전한 보조 구조다.

## 아키텍처 요약

```text
Player Text Input
-> Context Monitoring Layer
-> Safety Gate
-> ONN-C State Engine
-> MND-N Core
   -> Flourishing State Layer
   -> Context Monitoring Layer
   -> Keyes Signal Layer
   -> Support Recommendation Layer
   -> Response Generation Layer
-> Player Guidance / Onion State Transfer
```

핵심 원칙은 다음과 같다.

1. ONN-C는 성향 기반 시뮬레이션 대상이다.
2. MND-N은 PERMA와 Flourish를 참고하는 제3의 보조 도우미다.
3. Keyes 모델은 진단 라벨이 아니라 Green, Yellow, Red 주의 신호로만 사용한다.
4. 위기 신호가 감지되면 게임화된 조언을 중단한다.
5. 사용자나 캐릭터에게 병리적 라벨을 붙이지 않는다.
