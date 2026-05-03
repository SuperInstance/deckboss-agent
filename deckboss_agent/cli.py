"""CLI entry point for deckboss-agent."""
import argparse
import json
from datetime import datetime, timezone

from deckboss_agent import DeckBossAgent


def interactive_catch(agent: DeckBossAgent) -> None:
    print("=== DeckBoss Agent — Catch Processing Log ===")
    print()

    species = input("Species: ").strip()
    weight = input("Weight (lbs): ").strip()
    processing_method = input("Processing method: ").strip()
    crew_raw = input("Crew names (comma-separated): ").strip()
    crew_names = [c.strip() for c in crew_raw.split(",") if c.strip()]

    quality_grade = input("Quality grade (A/B/C): ").strip() or "A"
    storage_method = input("Storage method: ").strip()
    defects = input("Defects (if any): ").strip()
    notes = input("Additional notes: ").strip()

    print()
    result = agent.log_catch_processing(
        species, float(weight), processing_method, crew_names,
        quality_grade, storage_method, defects, notes
    )
    print(f"Catch logged. Tile: {result.get('tile_hash', '?')}")


def interactive_crew_assign(agent: DeckBossAgent) -> None:
    print("=== DeckBoss Agent — Crew Assignment ===")
    print()

    shift = input("Shift (day/night): ").strip() or "day"
    print("Crew assignments (name: role, one per line, empty line to finish):")
    assignments = {}
    while True:
        line = input().strip()
        if not line:
            break
        if ":" in line:
            name, role = line.split(":", 1)
            assignments[name.strip()] = role.strip()

    notes = input("Notes: ").strip()

    print()
    result = agent.assign_deck_crew(assignments, shift, notes)
    print(f"Assignment logged. Tile: {result.get('tile_hash', '?')}")


def interactive_equipment(agent: DeckBossAgent) -> None:
    print("=== DeckBoss Agent — Equipment Status ===")
    print()

    equipment_name = input("Equipment name: ").strip()
    status = input("Status (operational/maintenance/broken): ").strip()
    condition = input("Condition (good/fair/poor): ").strip() or "good"
    maintenance_due = input("Maintenance due date: ").strip()
    notes = input("Notes: ").strip()

    print()
    result = agent.log_equipment_status(equipment_name, status, condition, maintenance_due, notes)
    print(f"Equipment logged. Tile: {result.get('tile_hash', '?')}")


def handle_status(agent: DeckBossAgent) -> None:
    status = agent.get_status()
    print(json.dumps(status, indent=2, default=str))


def handle_catch_history(agent: DeckBossAgent) -> None:
    records = agent.get_catch_history()
    catch_records = [t for t in records if "Catch processed:" in t.get("question", "")]
    for i, t in enumerate(catch_records):
        print(f"[{i+1}] {t.get('question', 'unknown')}")
        print(f"    {t.get('answer', '')[:200]}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="DeckBoss Operations Intelligence")
    parser.add_argument("--vessel", default="unknown", help="Vessel name")
    parser.add_argument("--deck-boss", default="default", help="Deck boss ID")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--catch", action="store_true", help="Log catch processing")
    parser.add_argument("--crew", action="store_true", help="Assign deck crew")
    parser.add_argument("--equipment", action="store_true", help="Log equipment status")
    parser.add_argument("--status", action="store_true", help="Show deck status")
    parser.add_argument("--history", action="store_true", help="Show catch history")
    args = parser.parse_args()

    agent = DeckBossAgent(vessel=args.vessel, deck_boss=args.deck_boss, verbose=args.verbose)

    if args.catch:
        interactive_catch(agent)
    elif args.crew:
        interactive_crew_assign(agent)
    elif args.equipment:
        interactive_equipment(agent)
    elif args.status:
        handle_status(agent)
    elif args.history:
        handle_catch_history(agent)
    else:
        print("DeckBoss Operations Intelligence")
        print("Use --catch, --crew, --equipment, --status, or --history")
        print("Run with --help for all options")


if __name__ == "__main__":
    main()