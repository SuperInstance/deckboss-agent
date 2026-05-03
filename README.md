# deckboss-agent

**Deck Operations Intelligence** for [deckboss.ai](https://deckboss.ai) — catch processing logs, deck crew coordination, and equipment tracking powered by PLATO.

## Features

- **Catch Processing Logs**: Record species, weight, processing method, quality grade, and defects
- **Crew Coordination**: Assign deck crew to shifts and log activities
- **Equipment Tracking**: Track equipment status, condition, and maintenance schedules
- **Status Overview**: Get a snapshot of deck operations

## Installation

```bash
pip install deckboss-agent
```

## Usage

```bash
# Log catch processing
deckboss --catch

# Assign deck crew
deckboss --crew

# Log equipment status
deckboss --equipment

# Check deck status
deckboss --status

# View catch history
deckboss --history
```

## PLATO Integration

Communicates with PLATO tile server at `http://localhost:8847`. All deck operations are logged as tiles in the `deckboss-ai` room.

## License

MIT
## Related

- [deckboss.ai](https://deckboss.ai) — Live site
- [deckboss-ai-pages](https://github.com/SuperInstance/deckboss-ai-pages) — GitHub Pages source
