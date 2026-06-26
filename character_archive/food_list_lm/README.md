![Project](https://img.shields.io/badge/Project-MaAM-blue)
![Contest](https://img.shields.io/badge/Type-Kitchen_Contest-orange)
![Category](https://img.shields.io/badge/Category-Food_Game-Skyblue)
![Status](https://img.shields.io/badge/Status-Prototype-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

![MaAM Kitchen Contest](../../data/images/lm/banner.png)

# MaAM Kitchen Contest

**MaAM Kitchen Contest** is a concept project where MaAM lunch menu cards and food bots gather in one kitchen to prepare meals together.

This project is not just a collection of food cards.  
Each lunch menu card appears as a bot with its own role,  
NTR-N observes the nutrition balance,  
and the player chooses the best lunch combination through a small food game experiment.

> Real Food. Real Energy.  
> Eat Well, Live Well.

---

## 1. Project Concept

MaAM Kitchen Contest begins with the image of many food bots preparing lunch together in a shared kitchen.

Each bot represents one menu.

- The Udon bot prepares a warm noodle dish.
- The Curry Rice bot creates a filling meal.
- The Burger Set bot provides quick fullness and energy.
- The Donburi bot combines rice and toppings in one bowl.
- The Lunchbox bot organizes a balanced meal.
- NTR-N checks the nutrition balance of the whole meal.
- ONN-C supports ingredient preparation and kitchen workflow.

This kitchen is a place where competition and cooperation exist together.  
The bots prepare their own menus, but the final goal is to provide the most suitable lunch for the player.

---

## 2. Core Idea

```txt
Lunch Menu Cards
-> Food Bots
-> Kitchen Preparation
-> Nutrition Check
-> Player Choice
-> Lunch Result
```

MaAM Kitchen Contest begins with one question:

```txt
What should we eat for lunch today?
```

The project expands that simple question into cards, bots, nutrition balance, and short game rules.

---

## 3. Character Roles

| Entity | Role |
|------|------|
| NTR-N | Nutrition observer and balance checker |
| ONN-C | Kitchen assistant and made entity |
| UDN-LM | Udon lunch menu bot |
| CRR-LM | Curry rice lunch menu bot |
| HBG-LM | Burger set lunch menu bot |
| DNB-LM | Donburi lunch menu bot |
| BNT-LM | Lunchbox lunch menu bot |
| PHO-LM | Pho lunch menu bot |
| DKS-LM | Donkatsu lunch menu bot |

Each bot has its own food identity, energy type, and lunch balance.  
The contest does not decide the strongest food.  
It decides which food fits the current situation best.

---

## 4. Menu Card System

Each lunch menu card contains:

```txt
No
MaAM Code
Menu Name
Food Image
Food Bot Image
Taste Message
Role
Energy
Personality
Lunch Balance
Nutrition Score
NTR-N Comment
```

The card works as both a visual archive and a game object.

For example:

| No | Code | Menu |
|---:|------|------|
| 006 | DKS-LM | Donkatsu |
| 011 | PHO-LM | Pho |
| 016 | UDN-LM | Udon |
| 017 | CRR-LM | Curry Rice |
| 018 | HBG-LM | Burger Set |
| 019 | DNB-LM | Donburi |
| 020 | BNT-LM | Lunchbox |

---

## 5. Contest Rule Draft

### Mode A: 3-Minute Lunch Pick

A fast lunch decision mode.

```txt
1. Each player draws one lunch card.
2. NTR-N checks the balance score.
3. Players vote for the most suitable menu.
4. The menu with the highest support becomes today's lunch.
```

Good for:

- office lunch
- friends deciding quickly
- mobile web mini-game

---

### Mode B: 5-Minute Kitchen Contest

A small food bot competition mode.

```txt
1. Three menu bots enter the kitchen.
2. Each bot presents its energy, role, and personality.
3. NTR-N gives a balance comment.
4. Players choose based on taste, time, price, and nutrition.
5. The winning bot serves lunch.
```

Good for:

- casual party play
- lunch roulette replacement
- short web game prototype

---

### Mode C: 10-Minute Team Kitchen

A cooperative lunch composition mode.

```txt
1. Players split into food bot teams.
2. Each team chooses a main menu, side dish, and drink.
3. NTR-N checks the balance.
4. ONN-C checks the kitchen preparation flow.
5. The team with the best total meal balance wins.
```

Good for:

- group lunch planning
- food education
- MaAM card expansion

---

## 6. NTR-N Nutrition Check

NTR-N does not ban food.  
It observes balance.

NTR-N checks:

- protein
- carbohydrate
- fat
- fiber
- vitamin
- sodium
- meal speed
- fullness
- repeated menu risk

The goal is not to make every lunch perfectly healthy.  
The goal is to make the player aware of the meal pattern.

---

## 7. Visual Direction

The visual style should feel like:

- warm kitchen contest
- cute food robots
- clean MaAM card UI
- green and cream color palette
- rounded corners
- small nutrition panels
- lively but readable composition
- friendly cooking competition atmosphere

The kitchen scene should show many bots working together, not fighting.  
The contest is friendly, energetic, and food-centered.

---

## 8. Prototype Direction

The first prototype can be made as a simple web game.

```txt
Frontend  : HTML / CSS / JavaScript or React
Game Time : 3 to 10 minutes
Platform  : Mobile web
Join Flow : Invite code or shared link
Core Loop : Enter -> Draw card -> Vote -> Result
```

Minimum prototype:

```txt
1. Show 20 lunch cards
2. Let players join with a room code
3. Randomly assign or select cards
4. Vote for today's lunch
5. Show the winner with an NTR-N comment
```

---

## 9. Archive Structure Draft

```txt
src/entities/ntr-n/maam-kitchen-contest/
  README.md
  README_KO.md
  rules/
    3min_lunch_pick.md
    5min_kitchen_contest.md
    10min_team_kitchen.md
  cards/
    006_돈까스.md
    011_쌀국수.md
  images/
    maam_kitchen_contest.png
```

---

## 10. Roadmap

- [ ] Define 20 lunch menu card metadata
- [ ] Create 20 food bot archive documents
- [ ] Create MaAM Kitchen Contest main image
- [ ] Design 3-minute, 5-minute, and 10-minute rule modes
- [ ] Build a simple mobile web prototype
- [ ] Add NTR-N nutrition comment system
- [ ] Add room code based multiplayer flow
- [ ] Test with real lunch selection

---

## Archive Remarks

MaAM Kitchen Contest turns lunch selection into a small ritual.

The important question is not only what tastes best.  
It is also what fits the day, the people, the time, and the energy level.

Food bots prepare the meal.  
NTR-N observes the balance.  
ONN-C helps the kitchen move.  
The player chooses the final lunch.

This is where MaAM food cards become a playable kitchen.

---

## License & Creator

* **License**: MIT License
* **Project**: MaAM (Maker and Artifact Intelligence Made)
* **Creator**: **Limabella**
