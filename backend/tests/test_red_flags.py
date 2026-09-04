from app.safety.red_flags import RedFlagEngine


def test_chest_pain_with_breathing_difficulty_triggers_rule():
    engine = RedFlagEngine()
    hits = engine.evaluate({"chest_pain", "breathing_difficulty"})
    assert any(h["rule_id"] == "RF001" for h in hits)


def test_no_symptoms_triggers_nothing():
    engine = RedFlagEngine()
    assert engine.evaluate(set()) == []
