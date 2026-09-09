"""Execution of the !escape command and its gate/response state."""

import random

from history import record_command
from profiles import update_escape_best
from responses import (
    ESCAPE_FAIL_0,
    ESCAPE_FAIL_LOW,
    ESCAPE_FAIL_MID,
    ESCAPE_FAIL_HIGH,
    ESCAPE_FAIL_INSANE,
    ESCAPE_SUCCESS,
)

# Short-term memory keeps escape responses from feeling like raw RNG.
# Avoid recently used templates, but still allow them back naturally later.
recent_escape_responses = []
ESCAPE_RECENT_MEMORY = 4

# Per-gate pass chances. A player must pass every earlier gate to reach later ones.
ESCAPE_CHANCES = [
    0.98,  # Gate 1
    0.95,  # Gate 2
    0.90,  # Gate 3
    0.82,  # Gate 4
    0.72,  # Gate 5
    0.60,  # Gate 6
    0.48,  # Gate 7
    0.35,  # Gate 8
    0.23,  # Gate 9
    0.14,  # Gate 10
    0.08,  # Gate 11
    0.04,  # Gate 12
]


def roll_escape_gates():
    """Roll the escape gates in order and return how many were cleared."""
    gates_passed = 0

    for chance in ESCAPE_CHANCES:
        if random.random() <= chance:
            gates_passed += 1
        else:
            break

    return gates_passed

def choose_escape_response(responses):
    """Choose an escape line while avoiding very recent repeats when possible."""
    # Prefer lines that have not been used recently.
    available = [
        response for response in responses
        if response not in recent_escape_responses
    ]

    # If a small pool has been exhausted, allow the full pool again.
    if not available:
        available = responses

    chosen = random.choice(available)

    recent_escape_responses.append(chosen)

    if len(recent_escape_responses) > ESCAPE_RECENT_MEMORY:
        recent_escape_responses.pop(0)

    return chosen


def run_escape(chatter_id, username, sassy_name):
    """Run the escape game using the name already resolved by the router."""
    record_command(
        chatter_id,
        username,
        "escape",
    )
    gates = roll_escape_gates()

    new_record, _old_best = update_escape_best(
        chatter_id,
        username,
        gates,
    )

    if gates == len(ESCAPE_CHANCES):
        template = choose_escape_response(ESCAPE_SUCCESS)

    elif gates == 0:
        template = choose_escape_response(ESCAPE_FAIL_0)

    elif gates <= 3:
        template = choose_escape_response(ESCAPE_FAIL_LOW)

    elif gates <= 6:
        template = choose_escape_response(ESCAPE_FAIL_MID)

    elif gates <= 9:
        template = choose_escape_response(ESCAPE_FAIL_HIGH)

    else:
        template = choose_escape_response(ESCAPE_FAIL_INSANE)

    gate_word = "gate" if gates == 1 else "gates"

    result = template.format(
        name=sassy_name,
        gates=gates,
        gate_word=gate_word,
    )

    if new_record:
        result += " NEW RECORD!"

    return result
