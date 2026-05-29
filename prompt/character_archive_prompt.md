좋습니다. 지금까지의 MoAM 구조를 보면 카드(Card)와 문서(Document)가 같은 아카이브 체계를 공유해야 합니다.

제가 추천하는 것은:

* **N = Non-fiction (실존 인물)**
* **E = Entity (MoAM 오리지널 캐릭터)**
* **Index = 도감 번호**
* **Code = 약어 + Type**

예시

| Name               | Type | Index | Archive ID |
| ------------------ | ---- | ----- | ---------- |
| Chopin             | N    | 001   | CHP-N      |
| Goethe             | N    | 002   | GTH-N      |
| Marguerite Higgins | N    | 003   | MGH-N      |
| Bill Shinn         | N    | 004   | BSH-N      |
| Baek Gijun         | E    | 001   | BKG-E      |
| Trio Robot         | E    | 002   | TRR-E      |

그러면 카드와 문서가 모두 동일한 아카이브 규칙을 따르게 됩니다.

아래는 이를 반영한 **character_archive_prompt v1** 입니다.

# character_archive_prompt

## SYSTEM RULE

Generate a MoAM Character Archive Document.

The document must belong to the same universe as the MoAM Archive Card system.

This archive is a museum-style intelligence record describing a character, their impact, philosophy, legacy and symbolic meaning.

Never write like Wikipedia.

Never write like a school textbook.

Write like an official archive artifact.

---

# MoAM Classification Rule

Type:

N = Non-fiction Character

* Historical figures
* Scientists
* Artists
* Philosophers
* Journalists
* Inventors

Examples:

CHP-N
GTH-N
MGH-N
BSH-N

---

E = Entity Character

* Original MoAM characters
* Fictional archive entities
* AI beings
* Resonance artifacts

Examples:

BKG-E
TRR-E
CBP-E

---

# Archive Metadata

Display at top:

![Project](https://img.shields.io/badge/Project-MoAM-blue)

![Classification](https://img.shields.io/badge/Class-Artifact_Intelligence-darkblue)

![Type](https://img.shields.io/badge/Type-{TYPE}-{COLOR})

![Index](https://img.shields.io/badge/Archive-{INDEX}-green)

![Status](https://img.shields.io/badge/Status-Active_Resonance-orange)

![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

# INPUT VARIABLES

Character Name

Archive Code

Archive Type

Archive Index

Profession

Era

Theme

Legacy

---

# DOCUMENT STRUCTURE

## Identity

Basic archive information.

### Name

### Code

### Type

### Era

### Occupation

---

## Historical Context

Describe the world surrounding the character.

Why this individual emerged.

What challenge existed.

---

## Core Contribution

What changed because of this character.

Why history remembers them.

---

## Resonance Analysis

MoAM exclusive section.

Analyze:

* values
* ideas
* influence
* symbolic meaning

Why this archive still resonates today.

---

## Artifact Interpretation

Represent the character as a living archive.

What artifact would symbolize them.

Why.

---

## Legacy

Short summary.

Maximum 5 lines.

Museum plaque style.

---

# WRITING STYLE

Korean premium archive

Museum exhibition

Historical documentary

Intelligent

Elegant

Timeless

Readable

Never sensational

Never clickbait

Never fandom style

---

# OUTPUT GOAL

The document should feel like:

A page extracted from a future museum archive preserving human intelligence and cultural memory.

그리고 배지 규칙은 이렇게 자동 생성되게 하면 됩니다.

```md
![Project](https://img.shields.io/badge/Project-MoAM-blue)
![Classification](https://img.shields.io/badge/Class-Artifact_Intelligence-darkblue)
![Type](https://img.shields.io/badge/Type-N-red)
![Index](https://img.shields.io/badge/Archive-003-green)
![Status](https://img.shields.io/badge/Status-Active_Resonance-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
```

마거리트 히긴스라면:

```md
Type : N
Index : 003
Code : MGH-N
```

백기준이라면:

```md
Type : E
Index : 001
Code : BKG-E
```

이렇게 되면 카드, README, 위키, 도감 문서가 전부 동일한 MoAM 아카이브 체계 아래에서 관리됩니다.
