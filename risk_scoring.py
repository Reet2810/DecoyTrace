import sqlite3


def calculate_event_score(event_count):
    if event_count == 1:
        return 4
    elif event_count == 2:
        return 6
    elif event_count == 3:
        return 8
    elif event_count == 4:
        return 10
    elif event_count == 5:
        return 12
    elif event_count == 6:
        return 14
    elif event_count == 7:
        return 16
    elif event_count == 8:
        return 18
    else:
        return 20


def calculate_token_score(activity):
    unique_tokens = set()

    for event in activity:
        unique_tokens.add(event[1])

    token_count = len(unique_tokens)

    if token_count == 1:
        return 6
    elif token_count == 2:
        return 12
    elif token_count == 3:
        return 18
    elif token_count == 4:
        return 24
    else:
        return 30


def calculate_resource_score(activity):
    type_base = {
        "generic": 10,
        "configuration": 20,
        "credential": 30
    }

    sensitivity_modifier = {
        "low": 0,
        "medium": 10,
        "high": 20
    }

    highest_score = 0

    connection = sqlite3.connect('decoytrace.db')

    for event in activity:
        token = event[1]

        result = connection.execute(
            "SELECT type, sensitivity FROM tokens WHERE token = ?",
            (token,)
        ).fetchone()

        if result:
            token_type, sensitivity = result

            score = (
                type_base[token_type]
                + sensitivity_modifier[sensitivity]
            )

            highest_score = max(highest_score, score)

    connection.close()

    return highest_score

def calculate_risk_score(activity):
    event_score = calculate_event_score(len(activity))
    token_score = calculate_token_score(activity)
    resource_score = calculate_resource_score(activity)

    total_score = event_score + token_score + resource_score

    return total_score


def get_risk_level(score):
    if score <= 24:
        return "Low"
    elif score <= 49:
        return "Medium"
    elif score <= 74:
        return "High"
    else:
        return "Critical"