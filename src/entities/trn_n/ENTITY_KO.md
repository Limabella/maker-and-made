# 트레이너 봇 (TRN-N)
트레이너봇은 시각 기반 자세 교정 에이전트로, 사용자의 운동 자세를 분석하고 자연어 코칭을 제공합니다.

## 주요 기능
- 실시간 자세 추정 및 분석
- 운동 반복 횟수 카운팅
- 자세 오류 탐지 및 피드백
- 개인화된 코칭 메시지 생성

## 아키텍처
- Motion Analyzer: 관절 각도, 단계 분류
- LLM Coach: GPT-style 코칭
- State Tracker: 세션 관리

## 기술 스택
- Python
- OpenAI API (LLM 코칭)
- OpenCV (비디오 처리)
