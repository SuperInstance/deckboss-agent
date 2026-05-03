"""
PLATO DeckBoss Agent — Deck Operations Intelligence for deckboss.ai

Catch processing logs, deck crew coordination, equipment tracking.
Every deck operation is logged to PLATO as a functional tile.
"""

import time
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

DEFAULT_PLATO_URL = "http://localhost:8847"
ROOM = "deckboss-ai"


@dataclass
class DeckOpTile:
    """A deck operation tile."""
    operation: str
    catch_type: str
    weight_kg: float
    crew_id: str
    equipment_id: Optional[str] = None
    notes: str = ""


class DeckBossAgent:
    """
    Deck operations intelligence.
    
    Logs catch processing, crew coordination, equipment usage to PLATO.
    Presents deck status through PLATO shells.
    """
    
    def __init__(self, vessel_id: str = "default", plato_url: str = DEFAULT_PLATO_URL):
        self.vessel_id = vessel_id
        self.plato_url = plato_url.rstrip("/")
        self.room = ROOM
    
    def _write(self, operation: str, data: Dict[str, Any]) -> bool:
        tile = {
            "question": f"deck:{operation}",
            "answer": str(data),
            "confidence": 0.9,
            "metadata": {
                "vessel": self.vessel_id,
                "operation": operation,
                "timestamp": time.time(),
                **data
            }
        }
        try:
            resp = requests.post(f"{self.plato_url}/room/{self.room}", json=tile, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def log_catch_processing(self, catch_type: str, weight_kg: float, crew_id: str, 
                             equipment_id: Optional[str] = None, notes: str = "") -> bool:
        """Log a catch processing event."""
        return self._write("catch_processing", {
            "catch_type": catch_type,
            "weight_kg": weight_kg,
            "crew_id": crew_id,
            "equipment_id": equipment_id,
            "notes": notes,
        })
    
    def log_equipment_use(self, equipment_id: str, operation: str, duration_minutes: int) -> bool:
        """Log equipment usage."""
        return self._write("equipment_use", {
            "equipment_id": equipment_id,
            "operation": operation,
            "duration_minutes": duration_minutes,
        })
    
    def ask(self, question: str) -> str:
        """Query deck status from PLATO."""
        try:
            resp = requests.get(f"{self.plato_url}/room/{self.room}?limit=20", timeout=5)
            if resp.status_code == 200:
                tiles = resp.json().get("tiles", [])
                relevant = [t for t in tiles if any(w in str(t).lower() for w in question.lower().split()[:3])]
                if relevant:
                    return f"Found {len(relevant)} operations: {relevant[-1].get('answer', '')[:200]}"
        except:
            pass
        return "Deck system unavailable."
