# BlokusDuo — AI agents for a competitive turn-based strategy game

Research code + experiments exploring search and reinforcement learning for **Blokus Duo**. This project compares classical planning (Minimax, MCTS) and learned components (CNN evaluation/policy) across large-scale simulation.

---

## Mission

Understand what makes agents strong at spatial, combinatorial games by combining:
- principled search algorithms,
- learned evaluation functions,
- and rigorous simulation-based evaluation.

## Project intention

This repository is meant to be:
- a **research/engineering artifact** (reproducible experiments, analysis notebooks),
- a **portfolio piece** showcasing applied RL + search,
- and a foundation for future work (stronger training loops, faster simulation, better evaluation).

---

## Results at a glance

- Ran **hundreds of thousands of simulations** across multiple agent matchups
- Compared:
  - Minimax variants
  - MCTS (with/without neural guidance)
  - PPO (baseline RL approach)

> The README and notebooks summarize findings; the paper provides a deeper narrative.

---

## Paper / write-up

- Main paper: https://docs.google.com/document/d/1t95HiT_Vk48AHe5BSArWpV6ObkvVYfmjIF5mwMdtEJw/edit?usp=sharing  
(Consider also exporting a PDF into `docs/` so the repo is self-contained.)

---

## Demo / images

Recommended to add:
- `docs/images/board.png` — sample board state
- `docs/images/pieces.png` — pieces overview (you already have `pieces*.png`)
- `docs/images/results.png` — headline plot from comparisons

Example:
```text
docs/images/
├── board.png
├── pieces.png
└── results.png
