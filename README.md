# PLATO DeckBoss Agent

Deck Operations Intelligence for deckboss.ai. Catch processing → PLATO → deck coordination.

## Quick Start

```python
from deckboss_agent import DeckBossAgent

agent = DeckBossAgent(vessel_id="bluefin")
agent.log_catch_processing("tuna", 250.5, crew_id="mike", equipment_id="scale_1")
agent.log_equipment_use("winch_2", "hauling", 45)
print(agent.ask("what was processed today?"))
```

## Architecture

- Catch processing → PLATO tiles
- Equipment tracking → PLATO tiles
- Agent presents deck status through shells
