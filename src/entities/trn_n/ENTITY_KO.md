# 트레이너 봇 (Trainer Bot, TRN-N) 명세서
트레이너 봇은 다중 모달 추론(Multimodal Reasoning)을 통해 사용자의 운동 자세를 분석하는 지능형 시각 코칭 에이전트입니다. 단순한 기하학적 계산을 넘어, 시각적 맥락을 이해하고 자연어 코칭을 제공하는 것을 목표로 합니다.

## 1. 주요 기능 (Key Features)
실시간 자세 추정: MediaPipe를 활용해 33개의 신체 랜드마크를 추출하고 정밀한 관절 각도를 계산합니다.

운동 횟수 카운팅: 운동 단계(Phase)를 추적하여 정확한 횟수 카운트 및 세션 관리를 수행합니다.

다중 모달 오류 탐지: 기하학적 데이터(각도)와 시각적 의미 맥락(이미지 분석)을 결합하여 복잡한 자세 오류를 찾아냅니다.

개인화된 자연어 코칭: M-CoT(다중 모달 사고의 사슬) 전략을 사용하여 인간과 유사한 피드백을 생성합니다.

## 2. 시스템 아키텍처 (System Architecture)
Motion Analyzer (기하학 엔진): 신체 좌표의 수학적 분석 및 운동 상태 변화를 처리합니다.

Semantic Visual Reasoner (시각 지능): 로컬 MLLM 엔진(Ollama/Llama-3 Vision)으로, 시각적 맥락(예: "뒤꿈치 들림", "불안정한 시선")을 통해 자세가 틀린 '이유'를 해석합니다.

LLM Coach: 기하학적 엔진과 시각 지능 엔진의 출력을 통합하여 최종 코칭 메시지를 합성합니다.

State & Memory Tracker: memory.py를 통해 사용자 이력을 관리하고 장기적인 성과 추적 및 회고를 수행합니다.

## 3. 기술 스택 (Tech Stack)
언어: Python

컴퓨터 비전: OpenCV, MediaPipe

지능형 엔진: Ollama (Llava / Llama-3 Vision), OpenAI API

데이터 관리: JSON 기반 지속성 로깅

## 4. 다중 모달 확장 로드맵 (3단계 계획)
이 로드맵은 "A Survey on Multimodal Large Language Models" 논문의 핵심 개념을 TRN-N 생태계에 통합하는 과정입니다.

[1단계] 시각적 의미 추론 통합: 수치 데이터(예: "무릎 각도 85도")에 의미적 해석(예: "무릎이 안으로 말리고 있음")을 추가합니다. 이를 위해 소규모 다중 모달 모델(SMM)과 통신하는 VisualReasoner 클래스를 생성합니다.

[2단계] 이벤트 기반 LAVR (LLM 보조 시각 추론): 모든 프레임이 아닌 '결정적 순간'만 분석하여 로컬 PC 자원을 최적화합니다. 자세 이탈 감지나 반복 완료 등 특정 이벤트 발생 시에만 MLLM을 호출합니다.

[3단계] 다중 모달 CoT 및 의미론적 로깅: 랜드마크 관찰 → 시각적 맥락 교차 검증 → 진단 결론 도출 순서의 사고 체계를 구축합니다. 또한 memory.py를 업데이트하여 수치 데이터와 함께 MLLM의 맥락 분석 내용을 저장합니다.

## 5. 테스트 가이드 (동영상 파일 입력)
입력 소스 수정: trn_bot.py에서 cv2.VideoCapture(0)를 사용자의 동영상 파일 경로(예: cv2.VideoCapture('workout.mp4'))로 변경합니다.

로컬 MLLM 실행: Ollama 서버에서 ollama run llava 또는 llama3-vision이 실행 중인지 확인합니다.

로그 확인: 세션 종료 후 memory.json 파일을 확인하여 semantic_context 필드에 AI의 지능형 자세 묘사가 기록되었는지 확인합니다.

---

Q-former로 그림이미지 향상
DeepResearch 아키텍처
GraphRAG 아키텍처