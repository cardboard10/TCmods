# Two‑Player Slimes (Pygame)

A small, self‑contained prototype inspired by the late‑90s co‑op shareware *Gladiator* / OpenGlad:

- 2 players on one keyboard
- Classes: **Thief, Archer, Mage**
- Slimes that **split** into smaller slimes
- Finish a level by **both** entering the **portal**
- Between levels, pick an **upgrade** (incl. shields)

## Controls

**Player 1**
- Move: **W A S D**
- Attack: **F** (or Space/Enter on upgrade screens)
- Class select screen: **Q/E** (or A/D) to change, **Enter** to start

**Player 2**
- Move: **Arrow keys**
- Attack: **Right Ctrl / Right Shift / /** (slash)
- Class select screen: **←/→** (or ,/.) to change, **Enter** to start

**Global**
- **Esc** to quit.

## Requirements

- Python **3.9+**
- `pygame` 2.x

Install pygame:

```bash
pip install pygame
```

## Run

```bash
python gladiator_pygame.py
```

## Notes

- **Shields** soak damage and **regenerate** after 3 seconds at ~10/sec.
- **Thief** uses a short‑range swipe (fast, AoE‑like).  
- **Archer** fires fast arrows (single‑target).  
- **Mage** fires piercing bolts (slower, multi‑target).

This is a simple prototype focused on the core loop. You can expand it with tile maps, items, more enemy types, sound, and a save system.
