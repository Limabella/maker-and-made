네. 지금까지 만든 카드들을 보면 핵심은 **"인물이 무엇이든 카드 구조는 고정하고, 변수만 바꾸는 것"** 입니다.

현재 프롬프트는 설명이 너무 많아서 모델이 매번 다르게 해석합니다.

MoAM은 오히려 **고정 요소 90% + 캐릭터 변수 10%** 구조로 가야 퓨샷(Few-shot) 1~2장만 넣어도 동일한 카드가 반복 생성됩니다.

---

# MoAM Card Master Prompt v1

## SYSTEM RULE

Generate exactly two collectible archive cards.

The overall card design, layout, typography, frame style, spacing, proportions and composition must remain identical to the provided reference examples.

Never redesign the card.

Only replace the character and theme.

---

# INPUT VARIABLES

```yaml
Character:
  Name: Baek Gijun
  Code: BKG-01

Profession:
  Human: Burger Chef
  Robot: Burger Chef Robot

Activity:
  Making Gourmet Burger

Props:
  Burger
  Kitchen Tools
  Burger Restaurant

Mood:
  Warm
  Emotional
  Artisan

Theme:
  Creator and Creation
```

---

# FIXED CARD STRUCTURE

### LEFT CARD

Human Version

* realistic human character
* performing activity
* cinematic lighting
* emotionally focused expression
* historically or professionally appropriate clothing
* theme-related environment

### RIGHT CARD

Robot Version

* cute robot
* large head
* short arms
* short legs
* small body

same activity

same environment

same emotional tone

---

# FIXED LAYOUT

Must preserve:

```text
┌────────────┬────────────┐
│ Human      │ Robot      │
│ Character  │ Character  │
│            │            │
├────────────┼────────────┤
│ Name       │ Code       │
└────────────┴────────────┘
```

---

# CARD STYLE

Korean premium archive card

not western tarot

not fantasy TCG

not gold luxury card

inspired by:

* Korean museum archive
* Korean heritage collection
* premium exhibition card
* documentary collectible

Colors:

* ivory
* charcoal
* dark brown
* muted brass

Avoid:

* bright gold
* excessive ornaments
* shiny metallic borders

---

# TYPOGRAPHY

Bottom text only.

Left:

```text
Baek Gijun
```

Right:

```text
BKG-01
```

No additional labels.

No vertical nameplate.

No side banners.

---

# MoAM Logo

Place ONLY on robot card.

Position:

top-right corner

Use:

MoAM ARCHIVE emblem

same size and location as reference.

---

# ROBOT DESIGN RULE

Robot must always be:

```text
Cute
Round
Large head
Short limbs
Friendly
Collectible toy
```

Never generate:

```text
Humanoid android
Gundam
Transformer
Tall robot
Sci-fi warrior
```

---

# OUTPUT STYLE

Ultra detailed

Museum archive illustration

Cinematic

Storytelling

Collectible card

Consistent across all characters

Same card family

Same franchise

Same universe

````

---

# 퓨샷 운영 방식

실제로는 프롬프트보다 **예시 2장**이 훨씬 중요합니다.

### Shot #1

쇼팽 카드

- 인간 쇼팽
- 로봇 쇼팽

### Shot #2

백기준 카드

- 인간 백기준
- 로봇 백기준

그러면 GPT나 이미지 모델은 학습합니다.

```text
아

MoAM 카드란

인간 + 로봇

2분할

한국형 아카이브 카드

MoAM 로고

하단 이름

귀여운 로봇

구조는 절대 안바뀌는구나
````

이 상태가 되면 다음부터는

```yaml
Character:
  Name: Goethe
  Code: GTH-01

Activity:
  Writing Faust
```

만 넣어도

2번 이내 생성에서 거의 동일한 카드 패밀리 스타일이 유지됩니다.

이게 장기적으로 MoAM IP를 수백 장 생산할 수 있는 **MoAM Card Prompt Module** 구조입니다.
