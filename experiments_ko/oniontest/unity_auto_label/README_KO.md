# Unity 자동 모션 라벨링 실험

목표는 `onn_97_motion.glb` 안의 97개 모션을 Unity에서 자동으로 초벌 라벨링하는 것이다.

이 방식은 모션의 의미를 완벽히 판독하지 않는다. 대신 Unity가 읽은 `AnimationClip`의 길이, 위치 커브, 회전 커브, 움직임량을 계산해 다음과 같은 임시 라벨을 만든다.

- `idle_001`
- `micro_gesture_001`
- `small_gesture_001`
- `body_gesture_001`
- `strong_reaction_001`
- `locomotion_or_shift_001`
- `long_motion_001`

이후 사람이 Unity에서 재생해 보면서 `dark_idle`, `guarded_idle`, `happy_small`, `safety_pause` 같은 의미 라벨로 보정한다.

## 설치 위치

Unity 프로젝트 안에 다음처럼 복사한다.

```text
Assets/
  Editor/
    OnionMotionAutoLabeler.cs
```

현재 repo 기준 원본 스크립트 위치:

```text
experiments_ko/oniontest/unity_auto_label/Editor/OnionMotionAutoLabeler.cs
```

## 실행 순서

1. Unity 프로젝트를 연다.
2. GLB/FBX importer가 `onn_97_motion.glb`의 AnimationClip을 Unity AssetDatabase에 노출하는지 확인한다.
3. Project 창에서 `onn_97_motion.glb` 또는 애니메이션 클립들을 선택한다.
4. 메뉴에서 실행한다.

```text
Tools > Five Flavor Onion > Auto Label Selected Motions
```

5. 결과 파일을 확인한다.

```text
Assets/Onion/Generated/onion_motion_auto_labels.csv
Assets/Onion/Generated/onion_motion_auto_labels.json
```

## 선택 기능

라벨 이름으로 `.anim` 복제본을 만들고 싶다면 다음 메뉴를 실행한다.

```text
Tools > Five Flavor Onion > Duplicate Selected Motions As Named Anim Clips
```

결과:

```text
Assets/Onion/Generated/Clips/*.anim
```

원본 GLB/FBX는 수정하지 않는다.

## 한계

- Unity가 GLB의 AnimationClip을 AssetDatabase에 노출해야 한다.
- GLB importer에 따라 clip이 보이지 않을 수 있다.
- 자동 라벨은 의미 라벨이 아니라 특징 기반 임시 라벨이다.
- `happy`, `sad`, `dark` 같은 의미 이름은 최종 검수가 필요하다.

## 권장 다음 단계

1. 자동 라벨 CSV를 만든다.
2. Unity에서 클립을 하나씩 미리보기한다.
3. `auto_label` 옆에 `final_label` 컬럼을 추가한다.
4. Five Flavor Onion 상태와 `final_label`을 연결한다.

예시:

```csv
original_name,auto_label,final_label
NlaTrack,idle_001,bright_idle
NlaTrack.040,strong_reaction_003,guarded_reject
NlaTrack.070,long_motion_002,dark_idle
NlaTrack.096,idle_004,safety_pause
```
