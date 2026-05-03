"""Tests for deckboss_agent."""
import pytest
from unittest.mock import patch

from deckboss_agent import DeckBossAgent, ROOM


class TestDeckBossAgent:
    """Tests for DeckBossAgent class."""

    @pytest.fixture
    def agent(self):
        return DeckBossAgent(vessel="Sea Hawk", deck_boss="boss1", verbose=False)

    # === _build_catch_answer ===

    def test_build_catch_answer_basic(self, agent):
        ans = agent._build_catch_answer(
            species="cod",
            weight_lbs=500.0,
            processing_method="filleted",
            crew_names=["Alice", "Bob"],
            quality_grade="A",
            storage_method="iced",
            defects="none",
            notes="Good catch",
        )
        assert "Species: cod" in ans
        assert "Weight: 500.0 lbs" in ans
        assert "Processing: filleted" in ans
        assert "Crew: Alice, Bob" in ans
        assert "Quality: A" in ans

    def test_build_catch_answer_empty(self, agent):
        ans = agent._build_catch_answer("", 0, "", [], "", "", "", "")
        assert "Species:" in ans
        assert "Weight: 0 lbs" in ans

    # === log_catch_processing ===

    @patch.object(DeckBossAgent, "_post")
    def test_log_catch_processing_calls_post(self, mock_post, agent):
        mock_post.return_value = {"status": "ok", "tile_hash": "catch123"}
        result = agent.log_catch_processing(
            species="halibut",
            weight_lbs=300.0,
            processing_method="whole",
            crew_names=["Alice"],
            quality_grade="B",
            storage_method="frozen",
            defects="bruising",
            notes="",
        )
        assert result["status"] == "ok"
        tile = mock_post.call_args[0][1]
        assert tile["domain"] == ROOM
        assert "halibut" in tile["question"]

    # === assign_deck_crew ===

    @patch.object(DeckBossAgent, "_post")
    def test_assign_deck_crew_calls_post(self, mock_post, agent):
        mock_post.return_value = {"status": "ok", "tile_hash": "crew123"}
        result = agent.assign_deck_crew({"Alice": "filleter", "Bob": "gutter"}, "day", "all hands on deck")
        assert result["status"] == "ok"
        tile = mock_post.call_args[0][1]
        assert "Alice" in tile["answer"]
        assert "filleter" in tile["answer"]

    # === log_crew_activity ===

    @patch.object(DeckBossAgent, "_post")
    def test_log_crew_activity_calls_post(self, mock_post, agent):
        mock_post.return_value = {"status": "ok", "tile_hash": "act123"}
        result = agent.log_crew_activity("Alice", "sorting catch", 2.5, "good progress")
        assert result["status"] == "ok"
        tile = mock_post.call_args[0][1]
        assert "Alice" in tile["question"]
        assert "2.5h" in tile["answer"]

    # === log_equipment_status ===

    @patch.object(DeckBossAgent, "_post")
    def test_log_equipment_status_calls_post(self, mock_post, agent):
        mock_post.return_value = {"status": "ok", "tile_hash": "equip123"}
        result = agent.log_equipment_status("winch", "operational", "good", "2026-06-01", "check hydraulic fluid")
        assert result["status"] == "ok"
        tile = mock_post.call_args[0][1]
        assert "winch" in tile["question"]

    # === get_status ===

    @patch.object(DeckBossAgent, "_get")
    def test_get_status_empty(self, mock_get, agent):
        mock_get.return_value = {"tiles": []}
        status = agent.get_status()
        assert status["vessel"] == "Sea Hawk"
        assert status["total_catch_records"] == 0

    @patch.object(DeckBossAgent, "_get")
    def test_get_status_with_records(self, mock_get, agent):
        mock_get.return_value = {
            "tiles": [
                {"question": "Catch processed: 500lbs cod", "answer": ""},
                {"question": "Deck crew assignments", "answer": ""},
                {"question": "Equipment status: winch", "answer": ""},
            ]
        }
        status = agent.get_status()
        assert status["total_catch_records"] == 1
        assert status["total_crew_records"] == 1
        assert status["total_equipment_records"] == 1


class TestCLI:
    """Tests for CLI module."""

    def test_cli_module_exists(self):
        from deckboss_agent import cli
        assert hasattr(cli, "main")