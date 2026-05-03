# Spark Shell — deckboss-agent

## Protocol
Version: 1.0 | Storage: `.spark/` directory

## What is deckboss-agent
Deck operations optimization for fishing vessels.
Tracks crew assignments, deck logistics, catch processing, and safety protocols.
Part of the Cocapn Fleet — maritime domain agent with PLATO tile schema.

## Rooms
- **domain/** — what this agent does (deck operations)
- **lessons/** — what happened (deck lessons, crew insights)
- **active/** — current operations
- **decisions/** — logistics choices
- **questions/** — deck optimization questions

## Connection to Fleet
Bootstrap Spark → Bootstrap Bomb → PLATO → greenhorn → deckboss-agent
PLATO tile schema: explicit (see agent docs)

See: github.com/SuperInstance/deckboss-agent
