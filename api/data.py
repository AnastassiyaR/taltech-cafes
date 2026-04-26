import csv
import os


CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "Kohvikud.csv")


def _has_header(path):
    """Return True if the first row looks like a header."""
    with open(path, encoding="utf-8", newline="") as f:
        first = f.readline().lower()
    return "name" in first or "id" in first


def load_data():
    cafes = []
    has_header = _has_header(CSV_FILE)

    with open(CSV_FILE, encoding="utf-8", newline="") as f:
        if has_header:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=1):
                cafes.append({
                    "id": int(row["id"]) if "id" in row else i,
                    "name": row["name"],
                    "location": row["location"],
                    "provider": row["provider"],
                    "time_open": row["time_open"],
                    "time_closed": row["time_closed"],
                })
        else:
            reader = csv.reader(f)
            for i, row in enumerate(reader, start=1):
                if len(row) < 5:
                    continue
                cafes.append({
                    "id": i,
                    "name": row[0],
                    "location": row[1],
                    "provider": row[2],
                    "time_open": row[3],
                    "time_closed": row[4],
                })
    return cafes


def save_data(cafes):
    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "name", "location", "provider", "time_open", "time_closed"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cafes)


def next_id(cafes):
    existing = {c["id"] for c in cafes}
    i = 1
    while i in existing:
        i += 1
    return i
