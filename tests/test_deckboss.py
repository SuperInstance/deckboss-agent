from deckboss_agent import DeckBossAgent

def test_create_agent():
    a = DeckBossAgent("test_vessel")
    assert a.vessel_id == "test_vessel"
    
def test_log_catch():
    a = DeckBossAgent("test")
    # Would need PLATO running to work
    # Just test structure
    assert hasattr(a, 'log_catch_processing')
    assert hasattr(a, 'log_equipment_use')
    assert hasattr(a, 'ask')
