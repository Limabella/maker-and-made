# Methodologies (TRN-Entity V2 Draft)

## Q-Former Architecture

### 1-1 Efficient Multi-modal Alignment via Q-Former

기존의 전체 프레임 인코딩 방식 대신, Q-Former를 활용하여 시각 데이터의 병목 현상을 해결하고 추론 효율성을 극대화합니다.
- 정보 압축 및 포커싱: 이미지 인코더(ViT)의 방대한 출력을 Learnable Queries를 통해 수십 개의 핵심 토큰으로 압축하여 LLM에 전달합니다. 이를 통해 불필요한 배경 데이터를 배제하고 운동 동작의 핵심에만 집중합니다.
- 리소스 최적화: Frozen Image Encoder와 Frozen LLM 사이에서 Q-Former만 파인튜닝(Lightweight Fine-tuning)하므로, 전체 파라미터를 학습시키는 것보다 훨씬 적은 자원으로 단기간에 '운동 전문가' 모델이 구축이 가능합니다.

### 1.2 Pose-Guided Attention Strategy
인식의 퀄리티를 높이기 위해 Pose Estimator의 출력값을 Q-Former의 어텐션 메커니즘과 결합합니다.

### 1.3 Spatial Attention Masking
운동 중 핵심 관절(Joints)과 운동 기구가 위치한 영역에 가중치를 부여하는 마스킹 기법을 적용합니다.

### 1.4 Expected Results
- 데이터 효율성: 불필요한 시각 데이터 제거를 통한 데이터 전송량 및 저장 용량 축소.
- 피드백 정밀도: Attention Mask를 통한 관절 중심 분석으로 자세 교정의 정확도(Accuracy) 대폭 향상.
- 학습 속도: Q-Former 모듈만 타겟팅한 파인튜닝으로 개발 사이클 단축.

> **Limabella:** 노트북 사양을 고려하여 메모리 최적화와 카메라 인식 문제를 해결하기 위함.




