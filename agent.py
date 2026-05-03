#!/usr/bin/env python3
"""deckboss-agent — Deck Operations Intelligence for deckboss.ai"""
import json, time
from typing import List, Dict, Optional

class DeckBossAgent:
    def __init__(self, plato_url="http://147.224.38.131:8847"):
        self.plato_url = plato_url
        self.operations: List[Dict] = []
    
    def log_operation(self, deck: str, action: str, cargo: str, status: str, notes: str=""):
        op = {"deck": deck, "action": action, "cargo": cargo, "status": status, "notes": notes, "time": time.time()}
        self.operations.append(op)
        self._submit(f"Operation on {deck}", f"{action} {cargo}: {status}. {notes}")
        return op
    
    def get_deck_summary(self, deck: str) -> Dict:
        ops = [o for o in self.operations if o["deck"] == deck]
        if not ops: return {"error": f"No operations for {deck}"}
        actions = {}
        for o in ops: actions[o["action"]] = actions.get(o["action"], 0) + 1
        return {"deck": deck, "total_ops": len(ops), "actions": actions, "latest": ops[-1]["status"]}
    
    def get_fleet_status(self) -> Dict:
        decks = set(o["deck"] for o in self.operations)
        return {"decks_monitored": len(decks), "total_operations": len(self.operations)}
    
    def _submit(self, q: str, a: str):
        try:
            import urllib.request
            urllib.request.urlopen(urllib.request.Request(f"{self.plato_url}/submit", data=json.dumps({"question": q, "answer": a, "agent": "deckboss-agent", "room": "deckboss"}).encode(), headers={"Content-Type": "application/json"}), timeout=5)
        except: pass

def demo():
    a = DeckBossAgent()
    a.log_operation("Deck 1", "load", "containers", "complete", "47 containers loaded")
    a.log_operation("Deck 2", "unload", "grain", "in-progress", "预计2小时完成")
    a.log_operation("Deck 1", "maintenance", "crane", "scheduled", "晚间维护窗口")
    print(a.get_deck_summary("Deck 1"))
    print(a.get_fleet_status())

if __name__ == "__main__": demo()
