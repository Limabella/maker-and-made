# AI Model Architecture

This document defines the first-pass architecture for the character-based AI model system.

The goal is to separate public experimentation from private business-facing development while keeping the architecture simple enough to expand later.

---

## 1. Core Strategy

- `experimental_lab` is public-first.
- `dex`, `historical_hall`, and `literay_hall` are private-first.
- Each character is treated as a role node in a larger AI system, not as a standalone novelty.
- The system may combine `LLM`, `ML`, `DL`, pipeline logic, and agent orchestration depending on the character.

---

## 2. Folder Roles

### `experimental_lab`
Public experimentation space.

- Purpose: rapid prototyping and validation
- Scope: openly shareable
- Main use: early experiments, paper-linked trials, feedback collection
- Technical level: start with simple pipeline and agent logic

Recommended characters:
- `MND`: mental care and counseling experiments
- `NTR`: nutrition and health data experiments
- `TRN`: human motion and video experiments

### `dex`
Advanced research space.

- Purpose: deep model work and higher-value AI development
- Scope: private-first
- Main use: competitive model design, multimodal systems, advanced pipelines
- Technical level: ML/DL-heavy architecture

Recommended direction:
- stronger inference
- ensemble systems
- service-oriented experimentation

### `historical_hall`
Historical character space.

- Purpose: low-level pipelines and agents based on historical figures
- Scope: private-first
- Main use: NPC-style operation, support agents, lightweight orchestration
- Caution: copyright, rights, and historical representation sensitivity

Recommended direction:
- start with simple pipelines
- increase sophistication only when needed
- review legal and ethical exposure before public release

### `literay_hall`
Literary and creative space.

- Purpose: writing support, creative assistance, symbolic NPC roles
- Scope: private-first
- Main use: ghostwriting support, creative workflow, narrative character systems
- Technical level: pipeline first, agent later

Recommended direction:
- writing assistance
- character-based creative interface
- emotion and narrative-driven NPC design

---

## 3. Character Classification

### `experimental_lab`
- `MND`: emotional and psychological support experiments
- `NTR`: nutrition and lifestyle information experiments
- `TRN`: motion and vision tests

### `dex`
- `BKG-002`: competitive content / model experiment
- `TR-001`: trio-only ensemble music content

### `historical_hall`
- `CHPN`: music interpretation and creative output
- `CUR`: research-oriented query character
- `JMR`: language, corpus, and translation pipeline
- `WCM`: language, lexicography, and sentence-structure pipeline
- `LDV`: image generation and cover-art creation
- `MGH`: real-time newsletter and news intake agent
- `SLD`: war, harmony, and narrative interpretation character

### `literay_hall`
- `GTH`: ghostwriting and writing pipeline
- `MPH`: devil-character NPC
- `VCT`: creative-activity core character

---

## 4. Architecture Levels

All characters should be assigned one or more of the following levels.

### Level 1: Pipeline
- input normalization
- rule-based processing
- data collection
- draft generation

### Level 2: Agent
- tool usage
- flow control
- task branching
- simple interaction

### Level 3: ML
- classification
- prediction
- ranking
- pattern recognition

### Level 4: DL
- multimodal processing
- generation
- rich representation learning
- complex inference

Default allocation:
- `experimental_lab`: Level 1 to Level 2
- `historical_hall` and `literay_hall`: Level 1 to Level 2
- `dex`: Level 3 to Level 4

---

## 5. Private Test Priority

### Phase 1
- `experimental_lab / MND`
- `experimental_lab / TRN`

### Phase 2
- `experimental_lab / NTR`
- `historical_hall / JMR`
- `historical_hall / WCM`
- `historical_hall / LDV`

### Phase 3
- all `dex`
- all `literay_hall`

---

## 6. Public-Facing Principles

- Keep experiments small and isolated.
- Document lightly first, then expand after validation.
- Public documents should show direction, not everything.
- Keep business-sensitive details in private documents.
- Start historical or rights-sensitive characters at low operational levels.

---

## 7. Next Documents

Recommended follow-up docs:

- `PUBLIC_OVERVIEW.md`
- `INTERNAL_TEST_PLAN.md`
- `ENTITY_ROLE_MATRIX.md`
- `SAFETY_AND_RIGHTS.md`

---

## 8. Summary

`experimental_lab` is the public lab, `dex` is the deep research layer, and `historical_hall` plus `literay_hall` are private low-risk pipeline and agent zones.

