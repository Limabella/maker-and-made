# References

---

## Character AI

### 대규모 언어 모델 기반 역할 연기 에이전트: 현황, 과제 및 미래 동향

- arXiv: https://arxiv.org/abs/2601.10122
- 제출일: 2026-01-15
- DOI: https://doi.org/10.48550/arXiv.2601.10122
- 페이지: preprint 형식이라 전통적 페이지 번호는 없음
- 참고 위치: 서론과 핵심 기술 개요는 arXiv 본문 1부와 3부에서 확인 가능
- 적용 포인트:
  - 심리 척도 기반 캐릭터 모델링
  - 기억 증강 프롬프팅
  - 동기-상황 기반 행동 결정 제어
  - 역할 지식, 성격 충실성, 가치 정렬

### 자연어 성격 제어 기반 LLM 행동 에이전트

- ETASR: https://etasr.com/index.php/ETASR/article/view/12631
- DOI: https://doi.org/10.48084/etasr.12631
- 게재: Engineering, Technology & Applied Science Research, Vol. 15, No. 5, October 2025
- 페이지: 26827-26832
- 핵심 위치:
  - 초록: 26827
  - 도입/문제정의: 26827-26828
  - 제안 방법과 시스템 구조: 26828-26829
  - 메모리 모듈 설명: 26829
- 접수/수정/승인: 2025-06-08 / 2025-07-07, 2025-07-20 / 2025-07-23
- 적용 포인트:
  - OCEAN/Big Five 성격 모델을 NPC 행동 제어에 사용한다.
  - NPC traits, game state, environment를 prompt generator로 조합한다.
  - 복잡한 behavior tree 대신 자연어 prompt 기반 행동 제어를 실험한다.

---

## Personality and Risk Context

### 공감과 공격성의 관계: 어두운 4요소 성격의 매개효과

- KCI: https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003316966
- 확인된 서지: 남창형, 서종한. 2026. 한국심리학회지: 건강, 31(2), 429-456.
- 확인된 DOI: https://doi.org/10.17315/kjhp.2026.31.2.004
- 관련 페이지: 429-456
- 키워드: 공감, 공격성, 어두운 4요소 성격, 간접경로
- 적용 포인트:
  - Dark Tetrad는 공격성 경로 이해를 위한 보조 연구 맥락으로만 사용한다.
  - 개인 성격 테스트나 사용자 라벨링에는 사용하지 않는다.
  - 사이코패시, 사디즘 등은 안전 필터와 공격적 응답 억제 연구에만 연결한다.

---

## Working Rule

Five Flavor Onion에서 참고문헌은 다음 순서로 사용합니다.

1. Big Five/OCEAN 기반 성격 제어를 기본 모델로 둔다.
2. LLM 캐릭터 연구는 프롬프트, 기억, 동기, 평가 프레임으로 반영한다.
3. Dark Tetrad 연구는 안전성/공격성/공감 경로의 참고로만 둔다.
4. 사용자나 캐릭터에게 병리적 라벨을 붙이지 않는다. (보류)
