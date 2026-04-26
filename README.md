# TalTech Cafes

A Flask web application for managing cafes on the TalTech campus. Includes a REST API and a browser interface in a single project.

---

## Project Structure

```
taltech-cafes/
├── app.py              ← entry point, registers blueprints
├── Kohvikud.csv        ← cafe data (UTF-8)
├── requirements.txt
├── api/
│   ├── routes.py       ← REST API endpoints
│   ├── data.py         ← CSV read/write
│   └── helpers.py      ← validation and time logic
├── web/
│   └── routes.py       ← web page routes
└── templates/
    ├── base.html
    ├── index.html
    ├── add.html
    ├── edit.html
    └── search.html
```

---

## Getting Started

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/cafes` | Get all cafes |
| GET | `/api/cafes/<id>` | Get a single cafe by ID |
| GET | `/api/cafes/open?from=HH:MM&to=HH:MM` | Get cafes open during a time range |
| POST | `/api/cafes` | Add a new cafe |
| PUT | `/api/cafes/<id>` | Update an existing cafe |
| DELETE | `/api/cafes/<id>` | Delete a cafe |

### Example — add a cafe (POST)

```json
{
  "name": "Caffeine",
  "location": "Ehitajate tee 5",
  "provider": "Caffeine",
  "time_open": "08:00",
  "time_closed": "19:00"
}
```

### Example — search by hours (GET)

```
GET /api/cafes/open?from=18:30&to=21:00
```

Returns only cafes open for the **entire** requested period — e.g. Restoran Nuudel (11:00–22:00) and Pizzakiosk Tehnopol (11:00–21:00).

---

## Web Interface

- **Home** — table of all cafes with edit and delete buttons
- **Search by hours** — filter cafes by a time range
- **Add cafe** — form to create a new entry

---

## Dependencies

`flask`, `flask-cors`