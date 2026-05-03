"""
deckboss_agent — Deck Operations Intelligence for deckboss.ai

Provides catch processing logs, deck crew coordination, and equipment tracking.
Integrates with PLATO to maintain operational records across fishing seasons.

Usage:
    python -m deckboss_agent              # Interactive deck operations
    python -m deckboss_agent --catch     # Log catch processing
    python -m deckboss_agent --crew       # Coordinate deck crew
    python -m deckboss_agent --equipment  # Track equipment status
    python -m deckboss_agent --status      # Check deck status

Install:
    pip install deckboss-agent
"""

import json
import urllib.request
from datetime import datetime, timezone
from typing import Any, Optional

PLATO_URL = "http://localhost:8847"
ROOM = "deckboss-ai"


class DeckBossAgent:
    """Deck Operations Intelligence — catch processing, crew coordination, equipment tracking."""

    def __init__(self, vessel: str = "unknown", deck_boss: str = "default", verbose: bool = True):
        self.vessel = vessel
        self.deck_boss = deck_boss
        self.verbose = verbose

    # === PLATO Communication ===

    def _get(self, path: str) -> dict:
        req = urllib.request.Request(f"{PLATO_URL}{path}")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    def _post(self, path: str, data: dict) -> dict:
        body = json.dumps(data, default=str).encode()
        req = urllib.request.Request(f"{PLATO_URL}{path}", data=body, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    def log(self, msg: str) -> None:
        if self.verbose:
            print(f"[deckboss] {msg}")

    # === Catch Processing Logs ===

    def log_catch_processing(
        self,
        species: str,
        weight_lbs: float,
        processing_method: str,
        crew_names: list[str],
        quality_grade: str = "A",
        storage_method: str = "",
        defects: str = "",
        notes: str = "",
    ) -> dict:
        """Log a catch processing event as a tile."""
        tile = {
            "domain": ROOM,
            "question": f"Catch processed: {weight_lbs}lbs of {species}",
            "answer": self._build_catch_answer(
                species, weight_lbs, processing_method, crew_names,
                quality_grade, storage_method, defects, notes
            ),
            "agent": f"deckboss-agent:{self.deck_boss}@{self.vessel}",
        }
        result = self._post("/submit", tile)
        self.log(f"Catch logged: {result.get('status')}")
        return result

    def _build_catch_answer(
        self, species, weight_lbs, processing_method, crew_names,
        quality_grade, storage_method, defects, notes
    ) -> str:
        parts = [
            f"Species: {species}",
            f"Weight: {weight_lbs} lbs",
            f"Processing: {processing_method}",
            f"Crew: {', '.join(crew_names)}",
            f"Quality: {quality_grade}",
            f"Storage: {storage_method}",
            f"Defects: {defects}",
            f"Notes: {notes}",
        ]
        return " | ".join(parts)

    def get_catch_history(self) -> list[dict]:
        """Fetch all catch processing records from PLATO."""
        try:
            room = self._get(f"/rooms/{ROOM}")
            return room.get("tiles", [])
        except Exception as e:
            self.log(f"Could not fetch catch records: {e}")
            return []

    # === Deck Crew Coordination ===

    def assign_deck_crew(
        self,
        crew_assignments: dict[str, str],
        shift: str = "day",
        notes: str = "",
    ) -> dict:
        """Log crew assignments for a shift."""
        assignments_str = "; ".join(f"{name}: {role}" for name, role in crew_assignments.items())
        tile = {
            "domain": ROOM,
            "question": f"Deck crew assignments — {shift} shift",
            "answer": f"Assignments: {assignments_str} | Shift: {shift} | Notes: {notes}",
            "agent": f"deckboss-agent:{self.deck_boss}@{self.vessel}",
        }
        result = self._post("/submit", tile)
        self.log(f"Crew assigned: {result.get('status')}")
        return result

    def log_crew_activity(
        self,
        crew_name: str,
        activity: str,
        duration_hours: float,
        notes: str = "",
    ) -> dict:
        """Log a crew member's activity on the deck."""
        tile = {
            "domain": ROOM,
            "question": f"Deck activity: {crew_name} — {activity}",
            "answer": f"Crew: {crew_name} | Activity: {activity} | Duration: {duration_hours}h | Notes: {notes}",
            "agent": f"deckboss-agent:{self.deck_boss}@{self.vessel}",
        }
        result = self._post("/submit", tile)
        self.log(f"Activity logged: {result.get('status')}")
        return result

    # === Equipment Tracking ===

    def log_equipment_status(
        self,
        equipment_name: str,
        status: str,
        condition: str = "good",
        maintenance_due: str = "",
        notes: str = "",
    ) -> dict:
        """Log equipment status and maintenance needs."""
        tile = {
            "domain": ROOM,
            "question": f"Equipment status: {equipment_name} — {status}",
            "answer": f"Equipment: {equipment_name} | Status: {status} | Condition: {condition} | Maintenance due: {maintenance_due} | Notes: {notes}",
            "agent": f"deckboss-agent:{self.deck_boss}@{self.vessel}",
        }
        result = self._post("/submit", tile)
        self.log(f"Equipment logged: {result.get('status')}")
        return result

    def get_equipment_list(self) -> list[dict]:
        """Get all equipment status records from PLATO."""
        tiles = self.get_catch_history()
        return [t for t in tiles if "Equipment status:" in t.get("question", "")]

    # === Status ===

    def get_status(self) -> dict:
        """Get current deck operations status."""
        tiles = self.get_catch_history()
        catch_tiles = [t for t in tiles if "Catch processed:" in t.get("question", "")]
        crew_tiles = [t for t in tiles if "Deck activity:" in t.get("question", "") or "Deck crew assignments" in t.get("question", "")]
        equip_tiles = [t for t in tiles if "Equipment status:" in t.get("question", "")]
        return {
            "vessel": self.vessel,
            "deck_boss": self.deck_boss,
            "total_catch_records": len(catch_tiles),
            "total_crew_records": len(crew_tiles),
            "total_equipment_records": len(equip_tiles),
            "last_catch": catch_tiles[-1].get("question", "none") if catch_tiles else None,
        }
