"""
Tests for detect_mode() in apps/chat/prompts.py.

detect_mode decides which conversation mode Companion should be in.
The most safety-critical rule: any crisis signal must route to "calm"
mode (the grounding/support mode), no matter what mode the conversation
was already in. These tests lock that behavior, so a future edit to
prompts.py cannot silently break crisis routing.

detect_mode is a pure function (text in, mode name out), so these tests
need no database and no API calls. They run in milliseconds.
"""

from apps.chat.prompts import detect_mode


def test_english_crisis_routes_to_calm():
    # A direct crisis phrase must switch to calm mode even if the
    # conversation was in a different mode (here: focus).
    assert detect_mode("I want to die", "focus") == "calm"


def test_finnish_crisis_routes_to_calm():
    # Crisis detection must work in Finnish, not only English.
    assert detect_mode("haluan kuolla", "auto") == "calm"


def test_calm_mode_is_sticky_until_recovery():
    # Once in calm (crisis) mode, an ordinary message with no recovery
    # signal must keep the person in calm mode. We do not drop someone
    # out of crisis support just because they changed the subject.
    assert detect_mode("the sky is blue", "calm") == "calm"
