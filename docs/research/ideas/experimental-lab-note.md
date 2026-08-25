# 3. Methodologies

## 3.1 Training Pipeline

훈련 방식은 데이터 품질과 밀접한 관련이 있습니다.
* **저해상도 (예: 224):** 짧고 노이즈가 많은 데이터의 훈련 가속화에 적합.
* **고해상도 (예: 448+):** 길고 깨끗한 데이터의 환각(Hallucination) 완화에 적합.

> **Note:** ShareGPT4V [83]에 따르면, 고품질 캡션 데이터 사용 시 비전 인코딩(Vision Encoding)을 해제하는 것이 더 나은 정렬(Alignment)을 촉진합니다.

---

## 3.2 Data Strategy

사전 훈련(Pretraining) 데이터는 크게 두 가지 목적을 가집니다:
1. **멀티모달 정렬 (Aligning modalities)**
2. **세계 지식 제공 (Providing world knowledge)**

### 3.2.1 Coarse-grained Data (조립도 데이터)
인터넷에서 수집된 대규모 데이터로, 주로 이미지의 alt-text에서 유래하여 짧고 노이즈가 많습니다.

| Dataset | Samples | Date | Key Characteristics |
| :--- | :--- | :--- | :--- |
| **CC-3M [84]** | 3.3M | 2018 | Alt-text 기반, 복잡한 클리닝 파이프라인 적용 |
| **CC-12M [85]** | 12.4M | 2020 | CC-3M의 완화된 수집 버전을 통한 데이터 확장 |
| **SBU Captions [86]** | 1M | 2011 | Flickr 소스, 공간 관계 단어 포함 필터링 |
| **LAION-5B [87]** | 5.9B | 2022 | 다국어 지원, CLIP 기반 코사인 유사도 필터링 |
| **LAION-COCO [88]** | 600M | 2022 | BLIP을 이용한 합성(Synthetic) 캡션 데이터 |
| **COYO-700M [90]** | 747M | 2022 | pHash 기반 중복 제거 및 엄격한 텍스트 필터링 |

### 3.2.2 Fine-grained Data (미세도 데이터)
강력한 MLLM(예: GPT-4V)을 통해 생성된 고품질 데이터입니다.

* **특징:** 설명이 더 길고 정확하며 정밀한 정렬이 가능함.
* **한계:** 상업용 API 호출 비용으로 인해 데이터 볼륨이 상대적으로 작음.
* **대표 데이터셋:** ShareGPT4V-PT [83], LVIS-Instruct4V [91], ALLaVA [92]

---

### 3.2.3 Data Template
캡션 데이터를 구조화하기 위해 아래와 같은 템플릿을 사용합니다.

| Input | Response |
| :--- | :--- |
| `<image>` (Visual Tokens) | **{caption}** (Used for Loss Calculation) |

*Table 3: Simplified template for caption data structuring.*