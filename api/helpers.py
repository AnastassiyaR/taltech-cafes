import re


def validate_time(t: str) -> bool:
    """Return True if t is a valid HH:MM time string (00:00 - 23:59)."""
    if not isinstance(t, str):
        return False
    parts = t.split(":")
    if len(parts) != 2:
        return False
    try:
        h, m = int(parts[0]), int(parts[1])
    except ValueError:
        return False
    return 0 <= h <= 23 and 0 <= m <= 59


def validate_provider_field(value: str) -> bool:
    """Return True if value is non-empty and contains no digits."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    return bool(stripped) and not re.search(r'\d', stripped)


def validate_text_field(value: str) -> bool:
    """Return True if value is non-empty and not purely numeric. Used for 'name' and 'location'."""
    return bool(value) and bool(value.strip()) and not value.strip().isdigit()


def time_to_minutes(t: str) -> int:
    """'HH:MM' -> minutes since midnight"""
    h, m = map(int, t.split(":"))
    return h * 60 + m


def is_open_during(cafe: dict, from_time: str, to_time: str) -> bool:
    """Return True if cafe is open during the entire requested time range."""
    c_open = time_to_minutes(cafe["time_open"])
    c_closed = time_to_minutes(cafe["time_closed"])
    q_open = time_to_minutes(from_time)
    q_closed = time_to_minutes(to_time)
    return c_open <= q_open and c_closed >= q_closed
