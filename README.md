# Smart Expense Tracker API

A REST API for tracking personal expenses. Supports adding expenses, listing
them, filtering by category, calculating totals overall and per category, and
deleting by id. Built with FastAPI and Pydantic, with data persisted to a local
JSON file.

## Requirements

- Python 3.11 or newer (developed and tested on 3.14)

## Setup

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/Ghanavanth-T/smart-expense-tracker-api
cd smart-expense-tracker-api
python -m venv .venv
```

Activate it:

```bash
# Windows (PowerShell)
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn src.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Visiting the root URL redirects to the
interactive API documentation at `http://127.0.0.1:8000/docs`.

## Running the tests

From the repository root, with the virtual environment active:

```bash
pytest
```

## API Contract

| Method | Endpoint            | Behaviour                                      |
|--------|---------------------|------------------------------------------------|
| POST   | `/expenses`         | Creates an expense. Returns 201 + full object. |
| GET    | `/expenses`         | Lists all. Optional `?category=` filter.       |
| GET    | `/expenses/summary` | Overall total + per-category breakdown.        |
| DELETE | `/expenses/{id}`    | Deletes by id. 404 if not found.               |

### Expense fields

| Field      | Type   | Rules                                           |
|------------|--------|-------------------------------------------------|
| `id`       | string | UUID4, server-generated. Never client-supplied. |
| `title`    | string | Required, min length 1.                         |
| `amount`   | float  | Must be > 0.                                    |
| `category` | string | Free text, lowercased on input.                 |
| `date`     | date   | ISO format `YYYY-MM-DD`.                        |

### Example request

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Groceries", "amount": 250.50, "category": "food", "date": "2026-07-30"}'
```

## Data storage

Expenses are persisted to `data/expenses.json`, which is created automatically
on the first write. The directory is gitignored, so a fresh clone starts with an
empty expense list. A missing, empty, or unreadable data file is treated as an
empty list rather than an error, so the server always starts cleanly.

## Design notes

- `amount` is a `float` for scope reasons. Production code should use `Decimal`
  to avoid floating-point rounding errors on currency.
- `amount > 0` means refunds and negative adjustments are out of scope.
- Category is free text, normalised to lowercase on input, rather than a fixed
  enum — an enum would reject any category not anticipated up front.
- Summary values are rounded to two decimal places to avoid exposing
  floating-point artefacts in API responses.

## Bonus

The optional **OpenAPI/Swagger documentation** bonus is included: interactive
docs are generated automatically by FastAPI and available at `/docs`, with the
OpenAPI schema at `/openapi.json`.

## Tests

The test suite covers expense creation, id generation, category normalisation,
validation of invalid input, category filtering, summary totals, and deletion
including the not-found case. Each test runs against an isolated temporary data
file, so tests never read or modify real data.