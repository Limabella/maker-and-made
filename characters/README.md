# Character Registry

`characters/`는 프로젝트가 참조하는 캐릭터 원전입니다. 기존 문서 상단의
`Classification`, `Category`, `Object Class`, 상태 배지를 공식 분류의 원본으로
유지합니다. 실행 코드와 프로젝트별 역할은 `src/projects/`에 둡니다.

## 운영 캐릭터

| Character | 기존 핵심 분류 | 상태 | 참여 프로젝트 |
|---|---|---|---|
| [ONN-C](onn-c/README_KO.md) | Collective Intelligence / Made Entity | active | OnionTest, Manmi Journal, Kitchen Contest |
| [MND-N](mnd-n/README_KO.md) | Experimental / Support Entity | active | OnionTest |
| [TRN-N](trn-n/README_KO.md) | Experimental | joining | OnionTest |
| [NTR-N](ntr-n/README_KO.md) | Experimental | planned | OnionTest, Manmi Journal, Kitchen Contest |
| [CUR-N](cur-n/README_KO.md) | Researcher | planned | OnionTest |
| [JLC-N](jlc-n/README_KO.md) | Historical Intelligence / Culinary Educator | joining | Manmi Journal |
| [ATV-O](atv-o/README_KO.md) | Collective Intelligence / Maker Entity | joining | Manmi Journal |
| [BKG-O](bkg-o/README.md) | Maker Entity | joining | Manmi Journal |
| [KHAN-O](khan-o/README.md) | Maker Entity | joining | Manmi Journal |
| [MMR-C](mmr-c/README_KO.md) | Record Entity (운영 분류) | planned | Manmi Journal |
| [MCA-N](mca-n/README_KO.md) | Editorial Intelligence (운영 분류) | planned | Manmi Journal |
| [RYE-C](rye-c/README_KO.md) | Collective Intelligence / Made Entity | planned | MaAM roadmap |

`planned`와 `joining`은 현재 실행되지 않아도 구체적인 프로젝트 계약이나
로드맵이 있는 상태입니다. 그런 계획이 없는 캐릭터만 [`archived/`](archived/)로
이동합니다.

## 참조 규칙

1. 프로젝트는 캐릭터 폴더를 복사하거나 이동하지 않고 `character-roles.yaml`에서 참조합니다.
2. 캐릭터 고유 타입과 설정은 이 폴더, 프로젝트 역할과 권한은 `src/projects/`에서 관리합니다.
3. 이미지·3D 원본은 [`Le-vela/character-assets`](https://github.com/Le-vela/character-assets)가 기준 저장소입니다.
4. 모델 가중치와 실행 로그는 Git에 넣지 않고, 학습 설정·평가·로드맵만 추적합니다.